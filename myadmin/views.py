from django.shortcuts import render, redirect
import json
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import re
from users.views import passpattern, email_pattern, SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import smtplib
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import requests
import string
import random
from tournaments.models import regestration, tournaments
from users.models import usersdetails
from pubgtournament.settings import MYEMAIL, textlocalapikey
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
import urllib.request
import urllib.parse
from .forms import Tournamentform
from users.models import mymessages, wallet
from datetime import datetime


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    """
    Generate a random string of specified length using lowercase letters and digits.
    Useful for generating unique IDs (e.g. for messages or tokens).
    """
    return ''.join(random.choice(chars) for _ in range(size))


def unique_messageid_generator():
    """
    Generate a unique message ID for notifications/messages.
    Ensures the generated ID does not already exist in the `mymessages` table.
    """
    redem_new_id = random_string_generator(1)
    redem_new_id = f'message_{redem_new_id}'
    qs_exists = mymessages.objects.filter(messageid=redem_new_id).exists()
    if qs_exists:
        # If ID exists already — regenerate recursively
        return unique_messageid_generator()
    return redem_new_id


def sendemail(email, message, username):
    """
    Send an email containing given message to specified email address.
    Uses a pre-defined HTML template to format the message.
    """
    ctx = {
        'roomscredentials': 1,
        'username': username,
        'message': message,
    }
    # Render the email template (path hardcoded — consider refactoring this)
    html_content = get_template(
        'C:/Users/Ayan/.../myadmin/templates/myadmin/sendcredentials.html'
    ).render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        html_content,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def sendpurposeemail(email, message, username, purpose):
    """
    Send an email for a specific purpose (e.g. tournament delay, cancellation).
    The purpose can be used inside the template for dynamic messaging.
    """
    ctx = {
        'username': username,
        'message': message,
        'purpose': purpose,
    }
    html_content = get_template(
        'C:/Users/Ayan/.../myadmin/templates/myadmin/sendcredentials.html'
    ).render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        html_content,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def sendsms(number, message):
    """
    Send SMS to given number using TextLocal (or similar) API.
    Encodes the request and sends it. Useful for sending quick alerts/credentials.
    """
    data = urllib.parse.urlencode({
        'apikey': textlocalapikey,
        'numbers': number,
        'message': message,
        'sender': 'TXTLCL',
        'test': True  # Consider setting this False in production
    }).encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    with urllib.request.urlopen(request, data) as f:
        _ = f.read()  # Response is ignored here


def give_token(email, firstname, lastname, password):
    """
    Generate a timed token (using itsdangerous) for secure operations like email verification.
    Returns a URL-safe token string.
    """
    s = serializer(SECRET_KEY, 1180)  # token expires in 1180 seconds (~20 min)
    token = s.dumps({
        'email': email,
        'firstname': firstname,
        'lastname': lastname,
        'password': password
    }).decode('utf-8')
    return token


def Emailverification(email, firstname, lastname, password):
    """
    Trigger sending of email verification link to a new admin user during registration.
    """
    token = give_token(email, firstname, lastname, password)
    link = f'http://localhost:8000/myadmin/admin/emailvalidation/{token}/'
    ctx = {
        'creaaccount': 1,
        'firstname': firstname,
        'link': link,
    }
    html_content = get_template(
        'C:/Users/Ayan/.../myadmin/templates/myadmin/sendcredentials.html'
    ).render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        html_content,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


def adminlogin(request):
    """
    Handle admin login.
    Checks credentials: email, password; ensures user is staff.
    On success — logs in and redirects to admin dashboard. Otherwise shows error.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        obj = User.objects.filter(email=email).first()
        if obj is not None and obj.is_staff and check_password(password, obj.password):
            login(request, obj)
            return redirect('MyADMIN')
        else:
            messages.success(request, 'Invalid Email And Password')
            return redirect('adminlogin')
    return render(request, 'myadmin/login.html')


def adminlogout(request):
    """Log out the current user (admin) and redirect to login page."""
    logout(request)
    return redirect('adminlogin')


def adminregister(request):
    """
    Handle staff/admin registration.
    Validates email & password (pattern), sends verification email.
    Displays errors if validation fails or user already exists.
    """
    if request.method == 'POST':
        context = {}
        email = request.POST.get('email')
        firstname = request.POST.get('name')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')

        matchemail = re.search(email_pattern, email)
        pass1 = re.search(passpattern, password)
        pass2 = re.search(passpattern, password2)
        admin = User.objects.filter(email=email).first()

        if (password == password2 and pass1 and pass2
                and admin is None and matchemail):
            Emailverification(email, firstname, lastname, password)
            messages.success(
                request,
                'A mail has been sent with a link to complete registration.'
            )
            return redirect('adminregister')

        if password != password2:
            context['nomatch'] = 1
        if admin is not None:
            context['userexists'] = 1

        return render(request, 'myadmin/register.html', context=context)

    return render(request, 'myadmin/register.html')


def adminemailvalidation(request, token):
    """
    Validate the token from verification email.
    On success — create staff user account. Otherwise show token-expired message.
    """
    try:
        s = serializer(SECRET_KEY)
        data = s.loads(token)
        username = unique_username_generator(data['firstname'])
        obj = User(
            username=username,
            first_name=data['firstname'],
            last_name=data['lastname'],
            email=data['email']
        )
        obj.is_staff = True
        obj.save()
        obj = User.objects.filter(email=data['email']).first()
        obj.set_password(data['password'])
        obj.save()
        messages.success(request, 'Your account has been created successfully!')
        return redirect('adminlogin')
    except Exception:
        messages.success(
            request,
            'Token expired for registration — please apply again.'
        )
        return redirect('adminregister')


@login_required(login_url='adminlogin')
def MyADMIN(request):
    """
    Admin dashboard view: lists all tournaments with status 0 or 3 (e.g. upcoming or started).
    For each tournament shows available and occupied seats ranges (for display in UI).
    """
    context = {}
    tours = {}
    if not request.user.is_staff:
        messages.success(request, 'Access Denied — no permission.')
        return redirect('adminlogin')

    tournament_list = tournaments.objects.filter(tourstatus__in=[0, 3])
    for t in tournament_list:
        tours[t] = {
            'availrange': range(t.availseats),
            'occupiedrange': range(t.occupiedseats)
        }
    context['tournaments'] = tours
    return render(request, 'myadmin/index.html', context=context)


def sendcredentails(request):
    """
    Send tournament credentials (room ID/password) to all registered users of a given tournament via SMS.
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        tour = tournaments.objects.get(pk=int(tourid))
        regs = regestration.objects.filter(tournament=tour)
        for reg in regs:
            reg_user = reg.user.user
            userphone = usersdetails.objects.filter(users=reg_user).first()
            message = (
                f'Hey {reg_user.first_name}, RoomID - {tour.roomid}, '
                f'RoomPassword - {tour.roompassword}. '
                'Good luck for the tournament!'
            )
            sendsms(userphone.phnumber1, message)
        data['smssend'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


def send_credentails_email(request):
    """
    Send tournament credentials via email to all registered users of a given tournament.
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        tour = tournaments.objects.get(pk=int(tourid))
        regs = regestration.objects.filter(tournament=tour)
        for reg in regs:
            reg_user = reg.user.user
            message = (
                f'RoomID - {tour.roomid}, RoomPassword - {tour.roompassword}. '
                'Good luck for the tournament!'
            )
            sendemail(reg_user.email, message, reg_user.first_name)
        data['emailssend'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


def canceltour(request):
    """
    Cancel a tournament (set its status to 2).
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 2
        tour.save()
        data['canceltour'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


def starttour(request):
    """
    Mark a tournament as started (status = 3).
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 3
        tour.save()
        data['canceltour'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


def completetour(request):
    """
    Mark a tournament as completed (status = 1).
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 1
        tour.save()
        data['canceltour'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


@login_required(login_url='adminlogin')
def activetournaments(request):
    """
    View listing active tournaments (status = 0) for admin.
    """
    context = {}
    tournament_list = tournaments.objects.filter(tourstatus=0)
    if tournament_list.exists():
        context['tournaments'] = tournament_list
    return render(request, 'myadmin/activetournaments.html', context=context)


@login_required(login_url='adminlogin')
def completetournaments(request):
    """
    View listing completed tournaments (status = 1) for admin.
    """
    context = {}
    tournament_list = tournaments.objects.filter(tourstatus=1)
    if tournament_list.exists():
        context['tournaments'] = tournament_list
    return render(request, 'myadmin/completetournaments.html', context=context)


@login_required(login_url='adminlogin')
def canceltournaments(request):
    """
    View listing cancelled tournaments (status = 2) for admin.
    """
    context = {}
    tournament_list = tournaments.objects.filter(tourstatus=2)
    if tournament_list.exists():
        context['tournaments'] = tournament_list
    return render(request, 'myadmin/canceltournaments.html', context=context)


@login_required(login_url='adminlogin')
def DetailsOfTournament(request, tourid):
    """
    Show details of a single tournament: info about the tournament,
    registered users, and — if finished — the winner’s user details.
    """
    context = {}
    tour = tournaments.objects.get(pk=int(tourid))
    users_registered = regestration.objects.filter(tournament=tour)
    context['tour'] = tour
    context['users'] = users_registered
    if tour.tourstatus == 1:  # if completed
        context['user'] = usersdetails.objects.filter(users=tour.winner).first()
    return render(request, 'myadmin/DetailsOfTournament.html', context=context)


def makewinner(request):
    """
    AJAX endpoint to declare a winner for a tournament.
    Updates tournament's winner and status to completed (1).
    """
    data = {}
    if request.method == 'POST':
        tourid = request.POST.get('tourid')
        regid = request.POST.get('regid')
        tour = tournaments.objects.get(pk=int(tourid))
        winner = regestration.objects.filter(sid=regid).first()
        tour.winner = winner.user.user
        tour.tourstatus = 1
        tour.save()
        data['winnerdeclared'] = 1
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )


@login_required(login_url='adminlogin')
def tournament(request, tourid):
    """
    View to display and edit tournament details via a form.
    Also handles rescheduling, cancellation, and notifying registered users of changes.
    """
    context = {}
    tour = tournaments.objects.get(pk=int(tourid))
    registered_users = regestration.objects.filter(tournament=tour)
    form = Tournamentform(instance=tour)

    if request.method == 'POST':
        form = Tournamentform(request.POST, instance=tour)
        if form.is_valid():
            try:
                # parse new and original tournament date
                date = datetime.strptime(request.POST.get('tourdate'), '%Y-%m-%d %H:%M:%S')
                tourdate = datetime.strptime(request.POST.get('initial-tourdate'),
                                              '%Y-%m-%d %H:%M:%S')
                tourdate_str = tourdate.strftime('%Y-%m-%d')
                newdate_str = date.strftime('%Y-%m-%d')
                if newdate_str != tourdate_str:
                    # If date changed — notify users about rescheduling
                    formatted = f"{date.strftime('%d')} {date.strftime('%b')}, {date.strftime('%Y')} at {date.strftime('%H:%M:%S')}"
                    for reg in registered_users:
                        useremail = reg.user.user.email
                        message = (f'Sorry for delay — {tour.tourname} date has been rescheduled. '
                                   f'New date: {formatted}')
                        sendpurposeemail(useremail, message,
                                         reg.user.user.first_name, 'Delay Message')
                        mymessage = mymessages(
                            messageid=unique_messageid_generator(),
                            user=reg.user.user,
                            message=message
                        )
                        mymessage.save()
            except Exception:
                # In case of parsing error — redirect without saving
                return redirect('tournament', tourid=tour.tourid)

            # Handle cancellation: refund entry fee, notify users
            if request.POST.get('tourstatus') == str(2):
                for reg in registered_users:
                    useremail = reg.user.user.email
                    message = (
                        f'{reg.user.user.first_name}, we are sorry to '
                        f'inform you that {tour.tourname} has been cancelled. '
                        'Your registration fee has been refunded to your wallet.'
                    )
                    sendpurposeemail(useremail, message,
                                     reg.user.user.first_name, 'Cancel Tournament')
                    mymessage = mymessages(
                        messageid=unique_messageid_generator(),
                        user=reg.user.user,
                        message=message
                    )
                    mymessage.save()
                    userwallet = wallet.objects.filter(user=reg.user.user).first()
                    userwallet.Balanceamt += tour.entryfee
                    mymessage = mymessages(
                        messageid=unique_messageid_generator(),
                        user=reg.user.user,
                        message=f'Credits have been added to your wallet.'
                    )
                    mymessage.save()
                    userwallet.save()

            form.save()
            messages.success(request, 'Changes have been saved successfully')
            return redirect('tournament', tourid=tour.tourid)

    context['form'] = form
    context['tour'] = tour
    context['registered_users'] = registered_users
    return render(request, 'myadmin/tournament.html', context=context)
