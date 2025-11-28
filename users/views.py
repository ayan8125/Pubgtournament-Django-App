import re
import random
import string
import urllib.request
import urllib.parse
import json
import requests
import datetime

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User

from users.models import user as UserGameMapping, rchoices, redem, wallet, usersdetails
from tournaments.models import regestration
from cashfree_sdk.payouts import Payouts
from cashfree_sdk.payouts.beneficiary import Beneficiary
from cashfree_sdk.payouts.transfers import Transfers
from cashfree_sdk.exceptions.exceptions import (
    BadRequestError,
    EntityDoesntExistError,
    InputWrongFormatError,
    IncorrectCredsError
)
from django_countries import countries
from pubgtournament.settings import textlocalapikey, MYEMAIL, SECRET_KEY


# —————————————————————————————————————————————————————
# Module-level configuration and regex patterns

email_pattern = re.compile(
    r'^([_\-\.a-zA-Z0-9]+)@([_\-\.a-zA-Z]+)\.([a-zA-Z]){2,7}$'
)
phonepattern = re.compile(r'^[0-9]{10}$')


# —————————————————————————————————————————————————————
# Utility functions (helpers, generators, external API wrappers)


def random_string_generator(size: int = 10,
                            chars: str = string.ascii_lowercase + string.digits
                            ) -> str:
    """Generate a random string of given size using the provided character set."""
    return ''.join(random.choice(chars) for _ in range(size))


def unique_username_id_generator(firstname: str) -> str:
    """
    Generate a unique username by combining firstname and random string.
    Ensures uniqueness across existing User objects.
    """
    candidate = f'Abok{firstname}_{random_string_generator(5)}'
    if User.objects.filter(username=candidate).exists():
        return unique_username_id_generator(firstname)
    return candidate


def unique_wallet_id_generator(firstname: str) -> str:
    """
    Generate a unique wallet ID combining firstname and random string.
    Ensures uniqueness across existing wallet objects.
    """
    candidate = f'wallet{firstname}_{random_string_generator(1)}'
    if wallet.objects.filter(walletid=candidate).exists():
        return unique_wallet_id_generator(firstname)
    return candidate


def give_token(email: str, name: str, phnumber: str, password: str,
               expiry: int = 11180) -> str:
    """
    Generate a time-limited token containing user info (email, name, phone, password).
    Useful for signup/email-verification flows.
    """
    s = Serializer(SECRET_KEY, expiry)
    token = s.dumps({
        'email': email,
        'name': name,
        'phnumber': phnumber,
        'password': password
    }).decode('utf-8')
    return token


def generate_otp(length: int = 6) -> str:
    """Generate a random alphanumeric OTP of given length."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def sendsms(tonumber: str) -> str:
    """
    Send an OTP via SMS using Textlocal API.
    Returns the generated OTP string.
    Note: In test mode ('test': True) — disable for production.
    """
    otp = generate_otp(6)
    message = (
        f'Your One Time Password (OTP) for account verification is {otp}. '
        'Do not share this OTP. It is valid only for a short time.'
    )
    data = urllib.parse.urlencode({
        'apikey': textlocalapikey,
        'numbers': tonumber,
        'message': message,
        'sender': 'TXTLCL',
        'test': True
    }).encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    with urllib.request.urlopen(request, data) as _:
        pass
    return otp


def send_email(link: str, email: str, firstname: str) -> None:
    """
    Send an email containing the provided link to the given email address.
    Used for operations like password reset or email verification.
    """
    ctx = {
        'firstname': firstname,
        'link': link,
        'resetmypassword': 1
    }
    html_content = get_template(
        'users/templates/users/setpassword.html'
    ).render(ctx)
    msg = EmailMultiAlternatives(
        subject='Account Verification',
        body=html_content,
        from_email=MYEMAIL,
        to=[email]
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


# —————————————————————————————————————————————————————
# User authentication / registration / profile-management views


def Signup(request):
    """Render the signup page (GET)."""
    return render(request, 'users/signup.html', {})


def Login(request):
    """Render the login page (GET)."""
    return render(request, 'users/Login.html', {})


def Logout(request):
    """Logout current user and redirect to home."""
    logout(request)
    return redirect('home')


def signup(request):
    """
    Handle signup POST: validate data, send SMS OTP if valid,
    return JSON response with status flags (errors or success).
    """
    data = {}
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        pnumber = request.POST.get('phnumber', '').strip()

        # Basic validations
        email_valid = bool(email_pattern.match(email))
        phone_valid = bool(phonepattern.match(pnumber))
        name_valid = name.replace(' ', '').isalpha()

        existing_user = User.objects.filter(email=email).first()
        existing_number = usersdetails.objects.filter(
            Q(phnumber1=pnumber) | Q(phnumber2=pnumber)
        ).first()

        if name_valid and email_valid and (existing_user is None) and (existing_number is None):
            otp = sendsms(pnumber)
            # Temporarily store user data for later password setting
            users_dicts[email] = [name, pnumber]
            response = HttpResponse(json.dumps({'otpsend': True}),
                                    content_type="application/json")
            response.set_cookie('XMHDABOOKCC', otp)
            return response

        # Populate error flags
        if not name_valid:
            data['notvalidname'] = True
        if existing_user is not None:
            data['emailexists'] = True
        if existing_number is not None:
            data['numberexists'] = True
        if not email_valid:
            data['notvalidemail'] = True
        if not phone_valid:
            data['notnumber'] = True

        return HttpResponse(json.dumps(data), content_type="application/json")


def set_password(request):
    """
    Handle password setting after signup. Send verification link via email to finalize registration.
    """
    if request.method == 'POST':
        password = request.POST.get('password')
        email = request.POST.get('email')

        if email not in users_dicts:
            return HttpResponse(status=400)

        name, pnumber = users_dicts[email]
        token = give_token(email, name, pnumber, password)
        link = f'{request.scheme}://{request.get_host()}/uservalidation/{token}/'

        send_email(link, email, name)
        messages.success(request,
                         'Verification link has been sent to your email. Please check your inbox.')
        return HttpResponse(json.dumps({'emailsend': 1}), content_type="application/json")

    return HttpResponse(status=405)  # Method not allowed


def otp_verification(request):
    """
    Verify OTP submitted by user during signup.
    """
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email = request.POST.get('email')

        if request.COOKIES.get('XMHDABOOKCC') == otp:
            return HttpResponse(json.dumps({'success': 1}),
                                content_type="application/json")
        return HttpResponse(json.dumps({'otpwrong': 1}), content_type="application/json")

    return HttpResponse(status=405)


def user_validation(request, token: str):
    """
    Validate token from email link; upon success create User, usersdetails, and wallet objects.
    """
    try:
        s = Serializer(SECRET_KEY)
        data = s.loads(token)

        email = data['email']
        name = data['name']
        phnumber = data['phnumber']
        password = data['password']

        username = unique_username_id_generator(name)
        user_obj = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)

        name_parts = name.split(' ')
        user_obj.first_name = name_parts[0]
        if len(name_parts) >= 2:
            user_obj.last_name = name_parts[1]
        user_obj.save()

        user_details = usersdetails(
            uid=unique_username_id_generator(name),
            phnumber1=phnumber,
            users=user_obj
        )
        user_details.save()

        user_wallet = wallet(
            walletid=unique_wallet_id_generator(name),
            user=user_obj,
            userdetail=user_details
        )
        user_wallet.save()

        messages.success(request, 'Your account has been created successfully.')
        return redirect('home')

    except Exception:
        # If token invalid or expired — cleanup and inform user
        for u in User.objects.filter(password=''):
            u.delete()
        return HttpResponse(
            '<h1>Your verification link is expired — please signup again.</h1>'
        )


def logins(request):
    """
    Handle AJAX login request — verify credentials and return JSON response.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_obj = User.objects.filter(email=email).first()

        if user_obj and check_password(password, user_obj.password):
            login(request, user_obj)
            return HttpResponse(json.dumps({'valid': 1}),
                                content_type="application/json")
        err = {'wrongpassword': 1} if user_obj else {'nouser': 1}
        return HttpResponse(json.dumps(err), content_type="application/json")

    return HttpResponse(status=405)


@login_required(login_url='Login')
def mymatch(request):
    """
    Display the authenticated user's confirmed tournament registrations,
    grouped by game.
    """
    user_game_map = UserGameMapping.objects.filter(user=request.user).first()
    regs = regestration.objects.filter(status=1, user=user_game_map)
    matches_by_game = {}
    for reg in regs:
        game = reg.tournament.game
        matches_by_game.setdefault(game, []).append(reg)

    return render(request, 'users/mymatch.html',
                  {'usermatch': matches_by_game} if matches_by_game else {})


@login_required(login_url='Login')
def account(request):
    """Render the account details page for the current user."""
    acc = usersdetails.objects.filter(users=request.user).first()
    return render(request, 'users/account.html',
                  {'user': request.user, 'account': acc})
