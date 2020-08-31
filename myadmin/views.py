from django.shortcuts import render,redirect
import json
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
import re
from users.views import passpattern,email_pattern,SECRET_KEY
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import smtplib
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
import requests
import string
import random
from tournaments.models import regestration, tournaments
from users.models import usersdetails 
from pubgtournament.settings import MYEMAIL,textlocalapikey
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail,EmailMultiAlternatives
import urllib.request
import urllib.parse
from .forms import Tournamentform
from users.models import mymessages, wallet
from datetime import datetime
import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_messageid_generator():
    redem_new_id= random_string_generator(1)
    redem_new_id = f'message_' + redem_new_id
    qs_exists= mymessages.objects.filter(messageid= redem_new_id).exists()
    if qs_exists:
        return unique_messageid_generator()
    return redem_new_id


def sendemail(email,message,username):
    ctx = {
        'roomscredentials':1,
        'username': username,
        'message': message,
    }
    message = get_template('C:/Users/Ayan/AppData/Local/Programs/Python/Python37/pubgtour/pubgtournament/myadmin/templates/myadmin/sendcredentials.html').render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        message,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(message, "text/html")
    msg.send()


def sendpurposeemail(email,message,username,purpose):
    ctx = {
        'username': username,
        'message': message,
        'purpose':purpose
    }
    message = get_template('C:/Users/Ayan/AppData/Local/Programs/Python/Python37/pubgtour/pubgtournament/myadmin/templates/myadmin/sendcredentials.html').render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        message,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(message, "text/html")
    msg.send()


def sendsms(number, message):    
    data =  urllib.parse.urlencode({'apikey': textlocalapikey, 'numbers': number,
        'message' : message, 'sender': 'TXTLCL','test':True})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()


def give_token(email,firstname,lastname,password):
    s = serializer(SECRET_KEY,1180)
    token = s.dumps({'email':email,'firstname':firstname,'lastname':lastname,'password':password}).decode('utf-8')
    return token

def Emailverification(email,firstname,lastname,password):
    token = give_token(email,firstname,lastname,password)
    link = 'http:localhost:8000/myadmin/admin/emailvalidation/'+ token + '/'
    ctx = {
        'creaaccount':1,
        'firstname': firstname,
        'link': link,
    }
    message = get_template('C:/Users/Ayan/AppData/Local/Programs/Python/Python37/pubgtour/pubgtournament/myadmin/templates/myadmin/sendcredentials.html').render(ctx)
    msg = EmailMultiAlternatives(
        'Subject',
        message,
        MYEMAIL,
        [email],
    )
    msg.attach_alternative(message, "text/html")
    msg.send()

# Create your views here.



def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        obj = User.objects.filter(email=email).first()
        ######print(obj)
        if obj != None and (obj.is_staff == True) and (check_password(password,obj.password) == True):
            login(request,obj)
            return redirect('MyADMIN')
        else:
            messages.success(request,'Invalid Email And Password')
            return redirect('adminlogin')
    return render(request,'myadmin/login.html')


def adminlogout(request):
    logout(request)
    return redirect('adminlogin')



def adminregister(request):
    if request.method == 'POST':
        context = {}
        email = request.POST['email']
        firstname  = request.POST['name']
        lastname  = request.POST['lastname']
        # pnumber = request.POST['phnumber']
        password = request.POST['password1']
        password2 = request.POST['password2']
        matchemail = re.search(email_pattern,email)
        pass1 = re.search(passpattern,password)
        pass2 = re.search(passpattern,password2)
        admin = User.objects.filter(email=email).first()
        if password == password2 and pass1 != None and pass2 != None and admin == None and matchemail != None:
            Emailverification(email,firstname,lastname,password)
            messages.success(request,'A mail has been Send with A link At your email address with Last Process of Registration.')
            return redirect('adminregister')
        if password != password2:
            context['nomatch'] = 1
        if admin != None:
            context['userexists'] = 1
        return render(request,'myadmin/register.html',context=context)
    return render(request,'myadmin/register.html')



def adminemailvalidation(request,token):
    try:
        s = serializer(SECRET_KEY)
        data = s.loads(token)
        username = unique_username_generator(data['firstname'])
        obj = User(username=username,first_name=data['firstname'],last_name=data['lastname'],email=data['email'])
        obj.is_staff = True
        obj.save()
        obj = User.objects.filter(email=data['email']).first()
        obj.set_password(data['password'])
        obj.save()
        messages.success(request,'You Acccount Has been Created Succesffuly!')
        return redirect('adminlogin')
    except:
        messages.success(request,'Token Is Expired for Regestration,Please Apply for Newone')
        return redirect('adminregister')





@login_required(login_url='adminlogin')
def MyADMIN(request):
    context = {}
    tours = {}
    if request.user.is_staff == False:
        messages.success(request,'Access Denied, You dont have Permission to access that page')
        return redirect('adminlogin')
    tournament = tournaments.objects.filter(tourstatus__in = [0,3] )
    for i in tournament:
        if i not in tours:
            tours[i] = {'availrange': range(i.availseats), 'occpiedrange': range(i.occupiedseats)}
    context['tournaments'] = tours
    return render(request,'myadmin/index.html',context=context)




def sendcredentails(request):
    data = {}
    if request.method == 'POST':
        tourid = request.POST['tourid']
        tour = tournaments.objects.get(pk=int(tourid))
        Users = regestration.objects.filter(tournament = tour) 
        for i in Users:
            regestereduser = i.user.user
            userphone = usersdetails.objects.filter(users = regestereduser).first()
            message = f'Hey , {regestereduser.first_name} RoomID - {tour.roomid}, RoomPassword - {tour.roompassword} are the credentials for ther Solo Beast Tournament. Thanks and bestofLuck for the tournament ,Atour.com'
            sendsms(userphone.phnumber1, message)
            print(userphone.phnumber1)

        data['smssend'] = 1
        return HttpResponse(json.dumps(data),  content_type="application/json")



def send_credentails_email(request):
    data = {}
    if request.method == 'POST':
        tourid = request.POST['tourid']
        tour = tournaments.objects.get(pk=int(tourid))
        Users = regestration.objects.filter(tournament = tour) 
        for i in Users:
            regestereduser = i.user.user
            message = f'RoomID - {tour.roomid}, RoomPassword - {tour.roompassword} are the credentials for ther Solo Beast Tournament. Thanks and bestofLuck for the tournament ,Atour.com'
            sendemail(regestereduser.email, message, regestereduser.first_name)

        data['emailssend'] = 1
        return HttpResponse(json.dumps(data),  content_type="application/json")




def canceltour(request):
    data = {}
    if request.method == 'POST':
        tourid = request.POST['tourid']
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 2
        tour.save()
        data['canceltour'] = 1 
        return HttpResponse(json.dumps(data),  content_type="application/json")


def starttour(request):
    data = {}
    if request.method == 'POST':
        tourid = request.POST['tourid']
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 3
        tour.save()
        data['canceltour'] = 1
        return HttpResponse(json.dumps(data),  content_type="application/json")


def completetour(request):
    data = {}
    if request.method == 'POST':
        tourid = request.POST['tourid']
        tour = tournaments.objects.get(pk=int(tourid))
        tour.tourstatus = 1
        tour.save()
        data['canceltour'] = 1 
        return HttpResponse(json.dumps(data),  content_type="application/json")


@login_required(login_url='adminlogin')
def activetournaments(request):
    context = {} 
    tournament = tournaments.objects.filter(tourstatus = 0)
    if len(tournament) > 0:
        context['tournaments'] = tournament
    return render(request,'myadmin/activetournaments.html',context=context)

@login_required(login_url='adminlogin')
def completetournaments(request):
    context = {} 
    tournament = tournaments.objects.filter(tourstatus = 1)
    if len(tournament) > 0:
        context['tournaments'] = tournament
    return render(request,'myadmin/completetournaments.html',context=context)


@login_required(login_url='adminlogin')
def canceltournaments(request):
    context = {} 
    tournament = tournaments.objects.filter(tourstatus = 2)
    if len(tournament) > 0:
        context['tournaments'] = tournament
    return render(request,'myadmin/canceltournaments.html',context=context)



@login_required(login_url='adminlogin')
def DetailsOfTournament(request, tourid):
    context = {}
    tour = tournaments.objects.get(pk=int(tourid))
    user = regestration.objects.filter(tournament=tour)
    if tour.tourstatus == 1:
        context['user'] = usersdetails.objects.filter(users = tour.winner).first()
    context['tour'] = tour
    context['users'] = user

    return render(request,'myadmin/DetailsOfTournament.html',context=context)



def makewinner(request):
    data = {}
    print('came')
    if request.method == 'POST':
        tourid = request.POST['tourid']
        regid = request.POST['regid']
        print(tourid, regid)
        tour = tournaments.objects.get(pk=int(tourid))
        winner = regestration.objects.filter(sid = regid).first()
        tour.winner = winner.user.user
        tour.tourstatus = 1
        tour.save()
        data['winnerdeclared'] = 1 
        return HttpResponse(json.dumps(data),  content_type="application/json")


@login_required(login_url='adminlogin')
def tournament(request, tourid):
    context = {}
    tour = tournaments.objects.get(pk=int(tourid))
    regestereduser = regestration.objects.filter(tournament = tour)
    form = Tournamentform(instance= tour)
    if request.method == 'POST':
        form = Tournamentform(request.POST,instance= tour)
        if form.is_valid():
            try:
                date = request.POST['tourdate']
                tourdate = request.POST['initial-tourdate']
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                tourdate = datetime.strptime(tourdate, '%Y-%m-%d %H:%M:%S')
                tourdate = tourdate.strftime('%Y-%m-%d')
                newdate = date.strftime('%Y-%m-%d')
                if newdate != tourdate:

                    date = f"{date.strftime('%d')} {date.strftime('%b')}, {date.strftime('%Y')} at {date.strftime('%H:%M:%S')} {date.strftime('%I')}"
                    for i in regestereduser:
                        useremail = i.user.user.email
                        message = f'Sorry for delay, but {i.user.user.first_name} {tour.tourname} tournament date has been rescheduled, now it will be hosting on {date} '
                        sendpurposeemail(useremail, message, i.user.user.first_name, 'Delay Message')
                        mymessage = mymessages(messageid = unique_messageid_generator(),user=i.user.user,message = message)
                        mymessage.save()
            except:
                return redirect('tournament', tourid=tour.tourid)
                
            if request.POST['tourstatus'] == str(2):
                for i in regestereduser:
                    useremail = i.user.user.email
                    message = f'{i.user.user.first_name}, we are sorry to inform you that {tour.tourname} tournament has been cancelled and your regestration fess has been Refunded into your  Gamersjam Wallet please redem it from there.'
                    sendpurposeemail(useremail, message, i.user.user.first_name, 'Cancel Tournament')
                    mymessage = mymessages(messageid = unique_messageid_generator(), user=i.user.user,message = message)
                    mymessage.save()
                    userwallet = wallet.objects.filter(user= i.user.user).first()
                    userwallet.Balanceamt += tour.entryfee
                    message = f'{i.user.user.first_name} Credits have added to your wallet'
                    mymessage = mymessages(messageid = unique_messageid_generator(), user=i.user.user,message = message)
                    mymessage.save()
                    userwallet.save()
            form.save()
            messages.success(request,'Changes have been saved successfully')
            return redirect('tournament', tourid=tour.tourid)

    
    context['form'] = form
    context['tour'] = tour
    context['regestereduser'] = regestereduser
    return render(request,'myadmin/tournament.html', context=context)