from django.shortcuts import render, redirect
from users.models import user
from game.models import Game
from .models import tournaments, regestration
from django.http import HttpResponse
from django.contrib import messages
import string
import random
import razorpay
from django.contrib.auth.decorators import login_required
from users.models import wallet, usersdetails, user, mymessages
from django.db.models import Q
import datetime


def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    """
    Generate a random string of given size consisting of lowercase letters and digits.
    Used to create unique IDs for registrations.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_solo_id_generator(firstname):
    """
    Generate a unique solo registration ID by combining a prefix, the user's firstname,
    and a random string. Ensures the ID doesn't already exist in registrations.
    """
    order_new_id = random_string_generator(5)
    order_new_id = f'Solo{firstname}{order_new_id}'
    qs_exists = regestration.objects.filter(sid=order_new_id).exists()
    if qs_exists:
        # If generated ID already exists, recursively generate a new one
        return unique_solo_id_generator(firstname)
    return order_new_id


def home(request):
    """
    Homepage view: lists all upcoming tournaments (tourstatus=0).
    If user is authenticated, include their wallet info (and flag if balance negative).
    """
    context = {}
    tours = tournaments.objects.filter(tourstatus=0)
    if request.user.is_authenticated:
        userwallet = wallet.objects.filter(user=request.user).first()
        if userwallet and userwallet.Balanceamt < 0:
            # Flag negative balance — maybe restrict redemption/payments
            context["noredem"] = 1
        context['wallet'] = userwallet
    context['tours'] = tours
    return render(request, 'tournaments/home.html', context=context)


@login_required(login_url='login')
def Regestrations(request, game, tour): 
    """
    Handle registration for a solo tournament.
    - GET: render registration form (prefill user info if present).
    - POST: process registration; create user-game mapping if needed;
      update phone number if changed; check seat availability; create registration.
      If entry fee zero — confirm immediately. Else redirect to payment flow.
    """
    context = {}
    # Fetch the selected game and tournament
    pgame = Game.objects.get(pk=int(game))
    userobj = user.objects.filter(user=request.user, games=pgame).first()
    tournament = tournaments.objects.filter(tourid=int(tour)).first()
    solouser = regestration.objects.filter(user=userobj, tournament=tournament).first()
    userp = usersdetails.objects.filter(users=request.user).first()

    if request.method == 'POST':
        username = request.POST.get('username')
        number = request.POST.get('number')
        # If user-game mapping doesn't exist — create it
        if userobj is None:
            userobj = user(user=request.user, username=username, games=pgame)
            userobj.save()
        else:
            userobj.username = username  # update username if changed
            userobj.save()

        # Update phone number if changed
        if userp and str(number) != userp.phnumber1:
            userp.phnumber1 = number
            userp.save()

        if tournament.availseats > 0:
            # Seats available — create registration with unique sid
            sid = unique_solo_id_generator(userobj.user.first_name)
            regester = regestration(
                sid=sid,
                tournament=tournament,
                user=userobj,
                regestrationfee=tournament.entryfee
            )
            regester.save()

            if tournament.entryfee < 1:
                # Free tournament — confirm registration immediately
                tour = tournament
                tour.availseats -= 1
                tour.occupiedseats += 1
                regester.status = 1
                regester.save()
                tour.save()
                messages.success(
                    request,
                    'Congrats, You have been registered for this tournament. '
                    'RoomID AND password will be sent to you 15 min before tournament start.'
                )
                return redirect('home')
            # Paid entry — redirect to payment flow
            return redirect('Regestrationprox', regestrationid=regester.sid)
        else:
            # No seats left
            return HttpResponse(
                '<h1>Sorry, Registration is full. Please apply for next tournament</h1>'
            )

    # If user already registered
    if solouser is not None:
        if solouser.status == 0:
            return redirect('Regestrationprox', regestrationid=solouser.sid)
        if solouser.status == 1:
            # Already confirmed registration
            context['userisregestered'] = 1
            context['tournament'] = solouser.tournament
            messages.success(
                request,
                f'You are already registered for {solouser.tournament.tourname}. '
                'Best of luck — see you in the tournament.'
            )
            return redirect('home')

    # Prefill form with existing data if available
    if userobj is not None:
        context['username'] = userobj.username
    if userp is not None:
        context['userphone'] = userp.phnumber1
    if tournament.tournamenttype > 0:
        context['multipleuser'] = 1

    return render(request, 'tournaments/SoloRegestration.html', context=context)


@login_required(login_url='login')
def Regestrationprox(request, regestrationid):
    """
    Payment initiation view.
    If no payment order exists for this registration — create one using Razorpay.
    Populate context with order_id and amount to send to payment page.
    """
    context = {}
    solouser = regestration.objects.get(pk=regestrationid)
    userp = usersdetails.objects.filter(users=request.user).first()

    # If payment order not yet created
    if solouser.razorpayorderid == '':
        fee = solouser.regestrationfee
        client = razorpay.Client(auth=("*****", "******"))
        order_amount = fee * 100  # convert to smallest currency unit
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        order = client.order.create(dict(
            amount=order_amount,
            currency=order_currency,
            receipt=order_receipt,
            payment_capture='0'
        ))
        solouser.razorpayorderid = order['id']
        solouser.save()
        context['order_id'] = order['id']
        context['rsum'] = order_amount
    else:
        # Order already exists — reuse it
        context['order_id'] = solouser.razorpayorderid
        context['rsum'] = solouser.regestrationfee

    # Pass user info to template
    context['userphone'] = userp.phnumber1 if userp else ''
    context['username'] = solouser.user.username
    return render(request, 'tournaments/soloregestrationprox.html', context=context)


# @csrf_exempt  # If this is exposed as webhook, consider enabling CSRF exemption carefully
def handlepayment(request, response):
    """
    Handle Razorpay payment callback.
    Response expected in format: 'order_id+payment_id+signature'.
    On success — verify signature, update registration & tournament seat counts; on failure — delete registration.
    """
    responses = response.split('+')
    verify = len(responses)
    if verify == 3:
        try:
            client = razorpay.Client(auth=("******", "*****"))
            params_dict = {
                'razorpay_order_id': responses[0],
                'razorpay_payment_id': responses[1],
                'razorpay_signature': responses[2]
            }
            # Verify payment signature for security
            client.utility.verify_payment_signature(params_dict)

            obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
            tour = obj.tournament

            # Deduct one seat and mark registration confirmed
            tour.availseats -= 1
            tour.occupiedseats += 1
            obj.razorpaymentid = responses[1]
            obj.razorpaysignature = responses[2]
            obj.status = 1
            obj.save()
            tour.save()

            messages.success(
                request,
                'Congrats, You have been registered for this tournament. '
                'RoomID AND password will be sent to you 15 min before tournament start.'
            )
            return redirect('home')
        except Exception:
            # Payment verification failed — delete registration
            obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
            if obj:
                obj.delete()
            messages.success(request, 'Your Payment Transaction failed!')
            return redirect('home')
    else:
        # Invalid response format — delete registration
        obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
        if obj:
            obj.delete()
        messages.success(request, 'Your Payment Transaction failed!')
        return redirect('home')


def CancelRegestration(request, regestrationid):
    """
    Cancel registration (before payment) by deleting the registration record.
    """
    obj = regestration.objects.filter(razorpayorderid=regestrationid).first()
    if obj:
        obj.delete()
    messages.success(request, 'Your Registration process was cancelled.')
    return redirect('home')


def pasttournaments(request):
    """
    Show list of past tournaments (tourstatus=1).
    Also fetch winner and a few runner-up (or participants) details for display.
    """
    context = {}
    tours = tournaments.objects.filter(tourstatus=1)
    actualtours = {}

    for i in tours:
        if i not in actualtours:
            winner = i.winner
            winnerprofile = usersdetails.objects.filter(users=winner).first()
            winner_user = user.objects.filter(user=winner).first()
            regwinner = regestration.objects.filter(tournament=i, user=winner_user).first()

            # Collect other participants (excluding winner), limit to first few
            regestereduser = regestration.objects.filter(~Q(user=winner_user), tournament=i)
            runnerups = {}
            cnt = 1
            for j in regestereduser:
                if cnt < 5:
                    userprofile = usersdetails.objects.filter(users=j.user.user).first()
                    runnerups[j] = userprofile
                    cnt += 1
                else:
                    break

            actualtours[i] = {
                'winner': {regwinner: winnerprofile},
                'runnerup': runnerups
            }

    context['tours'] = actualtours
    return render(request, 'tournaments/pasttournaments.html', context=context)


def test(request):
    """
    A simple test view — likely used for debugging or template checking.
    """
    return render(request, 'tournaments/test.html')


def usernotification(request):
    """
    Display notifications/messages for authenticated user.
    Messages grouped by date (today vs older dates) and ordered by message date.
    """
    context = {}
    if request.user.is_authenticated:
        mynotify = mymessages.objects.filter(user=request.user).order_by('-mdate')
        mynotifydict = {}
        tdate = datetime.datetime.today()
        stdate = f'{tdate.strftime("%d")}/{tdate.strftime("%m")}/{tdate.strftime("%Y")}'
        cnt = 0
        for i in mynotify:
            if i.message_status == 0:
                cnt += 1
            mdate = i.mdate
            smdate = f'{mdate.strftime("%d")}/{mdate.strftime("%m")}/{mdate.strftime("%Y")}'
            time = f'{mdate.strftime("%I")}:{mdate.strftime("%M")}{mdate.strftime("%p")}'
            if smdate == stdate:
                # Group today's messages separately
                mynotifydict.setdefault('today', []).append([i, time])
            else:
                smdates = f'{mdate.strftime("%B")} {mdate.strftime("%d")},{mdate.strftime("%Y")}'
                mynotifydict.setdefault(smdates, []).append([i, time])
        context['mynotifydict'] = mynotifydict
    return render(request, 'tournaments/usermessages.html', context=context)
