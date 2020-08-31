from django.shortcuts import render, redirect
from users.models import user
from game.models import Game
from .models import  tournaments,regestration
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
    return ''.join(random.choice(chars) for _ in range(size))

def unique_solo_id_generator(firstname):
    order_new_id= random_string_generator(5)
    order_new_id = f'Solo{firstname}{order_new_id}'
    qs_exists = regestration.objects.filter(sid= order_new_id).exists()
    if qs_exists:
        return unique_solo_id_generator(firstname)
    return order_new_id

# Create your views here.
def home(request):
    context = {}
    tours = tournaments.objects.filter(tourstatus=0)
    if request.user.is_authenticated:
        userwallet = wallet.objects.filter(user=request.user).first()
        if userwallet.Balanceamt < 0:
            context["noredem"] = 1
        context['wallet'] = userwallet
    context['tours'] = tours
    return render(request,'tournaments/home.html',context=context)


@login_required(login_url='login')
def Regestrations(request, game, tour): 
    context = {}
    pgame = Game.objects.get(pk=int(game))
    userobj = user.objects.filter(user = request.user, games = pgame).first()
    tournament = tournaments.objects.filter(tourid = int(tour)).first()
    solouser = regestration.objects.filter(user=userobj, tournament = tournament).first()
    userp = usersdetails.objects.filter(users=request.user).first()
    if request.method == 'POST':
        username = request.POST['username']
        number = request.POST['number']
        if userobj == None:
            userobj = user(user= request.user, username = username, games= pgame )
            userobj.save()
        else:
            userobj.username = username
            userobj.save()
        if str(number) != userp.phnumber1:
            userp.phnumber1 = number
            userp.save()
        if tournament.availseats > 0:
            sid = unique_solo_id_generator(userobj.user.first_name)
            regester = regestration(sid=sid, tournament= tournament, user = userobj, regestrationfee = tournament.entryfee)
            regester.save()
            if tournament.entryfee < 1: # if no entry fee then simply confirm the user regestration
                tour = tournament
                tour.availseats -= 1
                tour.occupiedseats += 1
                regester.status = 1
                regester.save()
                tour.save()
                messages.success(request,'Congrats, You have been  registered for this tournament, RoomID AND password will be send to You before 15min, of tournament starting time.')
                return redirect('home')
            return redirect('Regestrationprox', regestrationid = regester.sid)
        else:
            return HttpResponse('<h1>Sorry, Regestration has been Full. Please apply for next tournament</h1>')
    if solouser != None:
        if solouser.status == 0:
            return redirect('Regestrationprox', regestrationid = solouser.sid)
        if solouser.status == 1:
            context['userisregestered'] = 1
            context['tournament'] = solouser.tournament
            messages.success(request,f'You are already registered, for {solouser.tournament.tourname} tournament,Besofluck and see you in the tournament.')
            return redirect('home')
    if userobj != None:
        context['username'] = userobj.username
    if tournament.tournamenttype > 0:
        context['multipleuser'] = 1
    context['userphone'] = userp.phnumber1
    return render(request,'tournaments/SoloRegestration.html',context=context)


@login_required(login_url='login')
def Regestrationprox(request, regestrationid):
    context = {} 
    solouser = regestration.objects.get(pk=regestrationid)
    userp = usersdetails.objects.filter(users=request.user).first()
    if solouser.razorpayorderid == '':
        fee = solouser.regestrationfee
        client = razorpay.Client(auth=("rzp_test_57quymdSuXAsSs", "ctdt2Oef5Uq5gpEVyGRpks6E"))
        order_amount = fee*100 #multiple amount by 100 , eg 10000 means 100.00 or 29935 == 299.35
        order_currency = 'INR'
        order_receipt = 'order_rcptid_11'
        order = client.order.create(dict(amount=(order_amount), currency=order_currency, receipt=order_receipt, payment_capture='0'))
        solouser.razorpayorderid = order['id']
        solouser.save()
        context['order_id'] = order['id']
        context['rsum'] = order_amount
    else:
        context['order_id'] = solouser.razorpayorderid
        context['rsum'] = solouser.regestrationfee
    context['userphone'] = userp.phnumber1
    context['username'] = solouser.user.username
    return render(request,'tournaments/soloregestrationprox.html', context=context)



#@csrf_exempt
def handlepayment(request,response):
    responses = response.split('+') 
    verify = len(responses)
    if verify == 3:
        try:
            client = razorpay.Client(auth=("rzp_test_57quymdSuXAsSs", "ctdt2Oef5Uq5gpEVyGRpks6E")) 
            params_dict = { 
                'razorpay_order_id': responses[0], 
                'razorpay_payment_id':responses[1],
                'razorpay_signature': responses[2]
            }
            client.utility.verify_payment_signature(params_dict)
            obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
            tour = obj.tournament
            tour.availseats -= 1
            tour.occupiedseats += 1
            obj.razorpaymentid = responses[1]
            obj.razorpaysignature = responses[2]
            obj.status = 1
            obj.save()
            tour.save()
        # token = give_token3(obj.orderid,obj.user.email)
        # strs = '/Books/Bookingorderconfirm/' + token + '/'
        # user = User.objects.filter(email = obj.user.email).first()
        # sendacknowledge(obj.user.email,obj.user.first_name)
        # login(request, user)
            messages.success(request,'Congrats, You have been  registered for this tournament, RoomID AND password will be send to You before 15min, of tournament starting time.')
            return redirect('home')
        except:
            obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
            obj.delete()
            messages.success(request,'Your Payment Transaction was failed!')
            return redirect('home')
    else:
        obj = regestration.objects.filter(razorpayorderid=responses[0]).first()
        obj.delete()
        messages.success(request,'Your Payment Transaction was failed!')
        return redirect('home')


def CancelRegestration(request, regestrationid):
    obj = regestration.objects.filter(razorpayorderid = regestrationid).first()
    obj.delete()
    messages.success(request, 'Your Regestration Process was failed.')
    return redirect('home')




def pasttournaments(request):
    context = {}
    tours = tournaments.objects.filter(tourstatus=1)
    actualtours = {}
    for i in tours:
        if i not in actualtours:
            winner = i.winner
            winnerprofile = usersdetails.objects.filter(users=winner).first()
            winner = user.objects.filter(user=winner).first()
            regwinner = regestration.objects.filter(tournament=i, user = winner).first()
            regestereduser = regestration.objects.filter(~Q(user=winner),tournament=i)
            winner = {regwinner:winnerprofile}
            regesuser = {}
            cnt = 1
            for j in regestereduser:
                if cnt < 5:
                    userprofile = usersdetails.objects.filter(users=j.user.user).first()
                    regesuser[j] = userprofile
                    cnt += 1
                else:
                    break
            actualtours[i] = {'winner':winner, 'runnerup': regesuser}

    context['tours'] = actualtours
    
    return render(request, 'tournaments/pasttournaments.html', context  =context)





def test(request):
    return render(request, 'tournaments/test.html')



def usernotification(request):
    context = {}
    if request.user.is_authenticated:
        mynotify = mymessages.objects.filter(
            user=request.user).order_by('-mdate')
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
                if 'today' not in mynotifydict:
                    mynotifydict['today'] = []
                mynotifydict['today'].append([i, time])
            else:
                smdates = f'{mdate.strftime("%B")} {mdate.strftime("%d")},{mdate.strftime("%Y")}'
                if smdates not in mynotifydict:
                    mynotifydict[smdates] = []
                    mynotifydict[smdates].append([i, time])
                else:
                    mynotifydict[smdates].append([i, time])
        context['mynotifydict'] = mynotifydict
        return render(request,'tournaments/usermessages.html', context=context)
    