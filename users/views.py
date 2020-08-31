import re
import random
import string
import urllib.request
import urllib.parse
import json
import requests
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from pubgtournament import settings
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import smtplib
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from pubgtournament.settings import textlocalapikey,MYEMAIL,MYPASSWORD,SECRET_KEY
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail,EmailMultiAlternatives
from django.contrib.auth.models import User
from users.models import user, rchoices, redem, wallet, usersdetails
from cashfree_sdk.payouts import Payouts
from cashfree_sdk.payouts.beneficiary import Beneficiary

from cashfree_sdk.payouts.transfers import Transfers
from tournaments.models import regestration
from django.utils import timezone
from cashfree_sdk.exceptions.exceptions import BadRequestError,EntityDoesntExistError, InputWrongFormatError, IncorrectCredsError
from django_countries import countries
# initialization of cashfee api




users_dicts = {}
email_pattern = re.compile(r'^([_\-\.a-zA-Z0-9]+)@([_\-\.a-zA-Z]+)\.([a-zA-Z]){2,7}$')
namepattern = re.compile(r'[a-zA-Z]+')
userpattern = re.compile(r'[a-zA-Z0-9\.\-_@]+')
passpattern = re.compile(r'[a-zA-Z0-9\.-_@]{8,}')
phonepattern = re.compile(r'[0-9]{10}')
zipcodepattern = re.compile(r'[0-9]{6}')

def givebankname(bname):
    for i in rchoices:
        if i[1] == bname:
            return i[0] 
    return -1


def create_Beneficiary(beneId, name, email, phone, bankAccount, ifsc, address1, city, stat,pincode):
    bene_add_response = Beneficiary.add(
    beneId = beneId,
    name = name,
    email = email, 
    phone = phone,
    bankAccount = bankAccount,
    ifsc = ifsc,  
    address1 = address1, 
    city = city, 
    stat = stat, 
    pincode = pincode,
    )
    return bene_add_response.json()

def Request_Transfer(beneId,transferId,amount):
    tresponse = Transfers.request_transfer(
        beneId = beneId,
        transferId = transferId,
        amount = amount, #"1.00"
    )
    return tresponse.json()

def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def unique_username_id_generator(firstname):
    order_new_id= random_string_generator(5)
    order_new_id = f'Abok{firstname}_' + order_new_id
    qs_exists= User.objects.filter(username= order_new_id).exists()
    if qs_exists:
        return unique_username_id_generator(firstname)
    return order_new_id

def unique_wallet_id_generator(firstname):
    order_new_id= random_string_generator(1)
    order_new_id = f'wallet{firstname}_' + order_new_id
    qs_exists= wallet.objects.filter(walletid= order_new_id).exists()
    if qs_exists:
        return unique_wallet_id_generator(firstname)
    return order_new_id

def unique_transferid_generator():
    redem_new_id= random_string_generator(5)
    redem_new_id = f'redem_' + redem_new_id
    qs_exists= redem.objects.filter(redemid= redem_new_id).exists()
    if qs_exists:
        return unique_transferid_generator()
    return redem_new_id

def give_token5(email,name, phnumber, password):
    s = serializer(SECRET_KEY,11180)
    token = s.dumps({'email':email,'name':name, 'phnumber': phnumber,'password':password}).decode('utf-8')
    return token


def give_emailresettoken(email,newemail):
    s = serializer(SECRET_KEY,11180)
    token = s.dumps({'email':email,'newemail':newemail}).decode('utf-8')
    return token

def give_passwordresettoken(email):
    s = serializer(SECRET_KEY,11180)
    token = s.dumps({'email':email}).decode('utf-8')
    return token

def generate_otp():
    strs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    otp = ''
    for i in range(6):
        otp += strs[ random.randint(0,(len(strs)-1))]
    return otp

def generate_string():
    strs = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789^@#$&*?'
    otp = ''
    for i in range(10):
        otp += strs[ random.randint(0,(len(strs)-1))]
    return otp


def sendsms(tonumber):
    otp = generate_otp()
    message = f'Your One Time Password(OTP) for Verification of ABookShelf Account is {otp}.Dont Share this with anyone and it is only valid for 120 secs' 
    data =  urllib.parse.urlencode({'apikey': textlocalapikey, 'numbers': tonumber,
        'message' : message, 'sender': 'TXTLCL','test':True})
    data = data.encode('utf-8')
    request = urllib.request.Request("https://api.textlocal.in/send/?")
    f = urllib.request.urlopen(request, data)
    fr = f.read()
    return otp
    
def send_email(link, email, firstname):
    ctx = {
        'firstname': firstname,
        'link': link,
        'resetmypassword':1
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
            
def sendresettoken(email, firstname):
    token = give_passwordresettoken(email)
    link = 'http://localhost:8000/resetmypassword/'+token+'/'
    send_email(link, email, firstname)


# Create your views here.

def Signup(request):
    context = {}
    return render(request,'users/signup.html',context=context)



def Login(request):
    context = {}
    return render(request,'users/Login.html',context=context)


def Logout(request):
    logout(request)
    return redirect('home')    


def signup(request):
    data = {}
    if request.method == 'POST':
        email = request.POST['email']
        firstname  = request.POST['name']
        pnumber = request.POST['phnumber']
        emailmatch = re.search(email_pattern,email)
        numbermatch = re.search(phonepattern,pnumber)
        fname = firstname.replace(' ','').isalpha()

        obj  =  User.objects.filter(email=email).first()
        obj2 = usersdetails.objects.filter(Q(phnumber1=(pnumber))|Q(phnumber2=(pnumber))).first()

        if fname == True and emailmatch != None  and obj  == None and obj2 == None:
            otp = sendsms(pnumber)
            data = {
                'otpsend':'true'
            }
            users_dicts[email] = [firstname,pnumber]
            response = HttpResponse(json.dumps(data),  content_type="application/json")
            response.set_cookie('XMHDABOOKCC',otp)
            return response
   
        if fname == False:
            data['notvalidname'] = 'true'
        if obj != None:
            data['emailexists'] = 'true'
        if obj2 != None:
            data['numberexists'] = 'true'
        if emailmatch == None:
            data['notvalidemail'] = 'true'
        if numbermatch == None:
            data['notnumber'] = 'true'
        #print(data)
        return HttpResponse(json.dumps(data),  content_type="application/json")
    


def setPassword(request):
    data = {}
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        print(users_dicts)
        users_dicts[email].append(password)
        dicts = users_dicts[email]
        link = give_token5(email, dicts[0], dicts[1], password)
        links = 'http://localhost:8000/uservalidation/'+link+'/'
    
        ctx = {
            'user':dicts[0],
            'links':links,
            'link':'{% url "uservalidation" links %}',

        }
        message = get_template('C:/Users/Ayan/AppData/Local/Programs/Python/Python37/pubgtour/pubgtournament/users/templates/users/setpassword.html').render(ctx)
        msg = EmailMultiAlternatives(
            'Subject',
            message,
            MYEMAIL,
            [email],
        )
        msg.attach_alternative(message, "text/html")
        msg.send()

        data = {
            'emailsend':1
        }
        messages.success(request,'verification link has been sent at your email.Please check yur inbox ')
        return HttpResponse(json.dumps(data), content_type="application/json")
        


def otp(request):
    data = {}
    if request.method == 'POST':
        otp = request.POST['otp']
        email  = request.POST['email']

        if request.COOKIES['XMHDABOOKCC'] == otp:
            data['success'] = 1
            return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data = {
                    'otpwrong':1
                }
        return HttpResponse(json.dumps(data),  content_type="application/json")


def uservalidation(request, token):
    s = serializer(SECRET_KEY)
    try:
        email = s.loads(token)['email']
        name = s.loads(token)['name']
        phnumber = s.loads(token)['phnumber']
        password = s.loads(token)['password']
        user = User.objects.create_user(unique_username_id_generator(name),email, password)
        if len(name.split(' ')) >= 2:
            user.first_name = name.split(' ')[0]
            user.last_name = name.split(' ')[1]
            user.save()
        else:
            user.first_name = name
            user.save()

        obj = usersdetails(uid = unique_username_id_generator(name),phnumber1= (phnumber), users = user)
        obj.save()
        userwallet = wallet(walletid = unique_wallet_id_generator(name), user = user, userdetail = obj)
        userwallet.save()
        messages.success(request, 'Your Account has been created successfully.' )
        return redirect('home')
    except:
        d = User.objects.filter(password='')
        for i in d:
            i.delete()
        return HttpResponse('<h1>Your Verification link is expired plese sigup again</h1>')
    


def logins(request):
    data = {}
    if request.method == 'POST':
        email = request.POST['email'] 
        password  = request.POST['password']
        user = User.objects.filter(email=email).first()
        #print(user, 'hereeeeeeeeeeeeeee')
        if user is not None:
            if check_password(password,user.password) == True:
                login(request,user)
                data = {'valid':1}
            else:
                data = {
                'wrongpassword':1
            }
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data ={'nouser':1}
        return HttpResponse(json.dumps(data),  content_type="application/json")



@login_required(login_url='Login')
def mymatch(request):
    context = {}
    usermatch = {}
    userobj = user.objects.filter(user=request.user).first()
    userregestrations = regestration.objects.filter(status=1,user=userobj)
    for i in userregestrations:
        if i.tournament.game not in usermatch:
            usermatch[i.tournament.game] = [i]
        else:
            usermatch[i.tournament.game].append(i)
    if len(usermatch ) > 0:
        context['usermatch'] = usermatch
    return render(request,'users/mymatch.html', context = context)


@login_required(login_url='Login')
def Account(request):
    context = {}
    context['user'] = request.user
    context['account'] = usersdetails.objects.filter(users=request.user).first()
    return render(request,'users/account.html', context = context)


def editname(request):
    data = {}
    if request.method == 'POST':
        fullname = request.POST['fullname']
        user = User.objects.filter(email = request.user.email).first()
        if fullname.replace(' ','').isalpha():
            fullname = fullname.split(' ')
            if len(fullname) == 2:
                user.first_name = fullname[0]
                user.last_name = fullname[1]
                user.save()
            else:
                user.first_name = fullname[0]
                user.save()
            data['valid'] = 1
            return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data['notvalid'] = 1
            return HttpResponse(json.dumps(data), content_type="application/json")

    
def editmail(request):
    data = {}
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email = request.user.email).first()
        userwithemail = User.objects.filter(email =email).first()
        emailmatch = re.search(email_pattern,email)
        if emailmatch != None:
            if userwithemail == None:
                link = give_emailresettoken(user.email,email)
                links = 'http://localhost:8000/emailreset/'+link+'/'
            
                ctx = {
                    'user':user.first_name,
                    'links':links,
                    'link':'{% url "emailreset" links %}',
                    'resetemail':1

                }
                message = get_template('C:/Users/Ayan/AppData/Local/Programs/Python/Python37/pubgtour/pubgtournament/users/templates/users/setpassword.html').render(ctx)
                msg = EmailMultiAlternatives(
                    'Subject',
                    message,
                    MYEMAIL,
                    [email],
                )
                msg.attach_alternative(message, "text/html")
                msg.send()

                data['valid'] = 1
                return HttpResponse(json.dumps(data),  content_type="application/json")
            else:
                data['userexits'] = 1
                return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data['notvalid'] = 1
            return HttpResponse(json.dumps(data), content_type="application/json")



def editpassword(request):
    data = {}
    if request.method == 'POST':
        currentpassword = request.POST['currentpassword']
        newpassword = request.POST['newpassword']
        confirmnewpassword = request.POST['confirmnewpassword']

        user = User.objects.filter(email = request.user.email).first()
 
    
        if check_password(currentpassword,request.user.password) == True:
            if newpassword == confirmnewpassword:
                user.set_password(newpassword)
                user.save()
                login(request, user)
                data['valid'] = 1
                return HttpResponse(json.dumps(data),  content_type="application/json")
            else:
                data['nomatch'] = 1
                return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data['notvalid'] = 1
            return HttpResponse(json.dumps(data), content_type="application/json")



def editnumber(request):
    data = {}
    if request.method == 'POST':
        number = request.POST['number']

        user = usersdetails.objects.filter(users = request.user).first()
        userwithnumber = usersdetails.objects.filter(Q(phnumber1=(number))|Q(phnumber2=(number))).first()
    
        if userwithnumber == None:
            otp = sendsms(number)
            data['otpsend'] = 1
            response =  HttpResponse(json.dumps(data),  content_type="application/json")
            response.set_cookie('XMHDABOOKCC',otp)
            return response
        else:
            if userwithnumber.users == request.user:
                if number == user.phnumber1:
                    data['nochange'] = 1
                    return HttpResponse(json.dumps(data),  content_type="application/json")
                elif number == user.phnumber2:
                    user.phnumber1 = user.phnumber2
                    user.save()
                    data['changesuccess'] = 1
                    return HttpResponse(json.dumps(data),  content_type="application/json")
            else:
                data['userexits'] = 1
                return HttpResponse(json.dumps(data),  content_type="application/json")
            

def checkotp(request):
    data = {}
    if request.method == 'POST':
        otp = request.POST['otp']
        number = request.POST['number']
        
        if request.COOKIES['XMHDABOOKCC'] == otp:
            user = usersdetails.objects.filter(users = request.user).first()
            user.phnumber1 = number
            user.save()
            data['valid'] = 1 
            return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data['notvalid'] = 1 
            return HttpResponse(json.dumps(data),  content_type="application/json")


def emailreset(request,token):
    s = serializer(SECRET_KEY)
    try:
        newemail = s.loads(token)['newemail']
        email = s.loads(token)['email']
        user = User.objects.filter(email=email).first()
        user.email = newemail
        user.save()
        messages.success(request, 'Your Email is changed  successfully.' )
        return redirect('home')
    except:
        return HttpResponse('<h1>Your Email reseting  link is expired.</h1>')
    


def setprofileimage(request):
    data = {}
    if request.method == 'POST':
        profileimage = request.FILES['myfile']
        user = usersdetails.objects.filter(users = request.user).first()
        user.userimage = profileimage
        user.save()
        data['valid'] = 1
        return HttpResponse(json.dumps(data),  content_type="application/json")

def postrequest1(bname,hname,accno,ifscode):
    paytmParams = { 
        "amount": 500,
        "method": "netbanking",
        "payment_capture": 1,
        "receipt": "BILL13375649",
        "currency": "INR",
        "bank_account": {
            "account_number": accno,
            "name": hname,
                "ifsc": ifscode
        }
    }
    post_data = json.dumps(paytmParams)
    url = "https://api.razorpay.com/v1/orders"
    response = requests.post(url, data = post_data,headers={  "Content-Type" : "application/json"},auth=(settings.myrazorpayapikeyid,settings.myrazorpayapikey)).json()
    return response


@login_required(login_url='Login')
def redemymoney(request):
    context = {}
    userwallet = wallet.objects.filter(user = request.user).first()
    if userwallet.Balanceamt <= 0:
        messages.success(request,'You cannot Redem Money , beacause you dont have enough  money in your wallet.')
        return redirect('home')
    if userwallet.userdetail.addresstatus == 0:
        return redirect('home')
    if userwallet.accoutno != '':
        context['wallet'] = userwallet
    return render(request, 'users/redemymoney.html', context =context)


def posttoredemmoney(request):
    data = {}
    if request.method == 'POST':
        hname = request.POST['holdername']
        accno = request.POST['accoutno']
        ifscode = request.POST['ifscode']
        wallets = wallet.objects.filter(user=request.user).first()
        responses = Payouts.init(settings.clientId, settings.clientSecret, "TEST")
        if wallets.accoutno != accno or wallets.holdername != hname or wallets.IFSC != ifscode:
            replace_bene = Beneficiary.replace_bene(wallets.walletid)
            wallets.holdername = hname
            wallets.accoutno = accno
            wallets.IFSC = ifscode
            wallets.save()
        amount = wallets.Balanceamt
        bene_details_response = ''
        try:
            bene_details_response = Beneficiary.get_bene_details(wallets.walletid)
            # bene_details_response_content = json.loads(bene_details_response.content)
            # print("get beneficary details")
            bene_details_response = bene_details_response.json()
            print(bene_details_response)
        except IncorrectCredsError as exception:
            data['servererror'] = 1
            messages.success(request, 'Sorry, your money transfering process has been failed , due to some server error.Please try again later.')
            return HttpResponse(json.dumps(data),  content_type="application/json")
        except EntityDoesntExistError  as err:
            try:
                bene_details_response = create_Beneficiary(wallets.walletid,request.user.first_name,request.user.email,wallets.userdetail.phnumber1, accno, ifscode, wallets.userdetail.address1, wallets.userdetail.city, wallets.userdetail.state, wallets.userdetail.pincode)
                print(bene_details_response)
            except InputWrongFormatError:
                errormessage = 'Invalid Account Mumber or  IFSC code!'
                data['errormessage'] = errormessage
                return HttpResponse(json.dumps(data),  content_type="application/json")

        if bene_details_response != '':
            if bene_details_response['subCode'] == "200":
                try:
                    transferid = unique_transferid_generator()
                    trequest = Request_Transfer(wallets.walletid, transferid, "1.00")
                    print(trequest)
                    if trequest['subCode'] == "201": #pending and pendeint and later success
                        redems = redem(redemid=transferid, redemamt=amount,user=request.user,wallets=wallets,redemstatus=2)
                        redems.save()
                        data['valid'] = 1
                        messages.success(request, 'Your Money has redemed Successfully , but your money Transfer request is pending at the bank. Incase , if Money is not transfered in your bank account, dont worry we will refund your money back into the Your wallet.')
                        return HttpResponse(json.dumps(data),  content_type="application/json")
                    else:
                        data['valid'] = 1
                        redems = redem(redemid=transferid, redemamt=amount,user=request.user,wallets=wallets,redemstatus=1)
                        redems.save()
                        messages.success(request, 'Your Money has redemed , and transfered into your bank account successfully.')
                        return HttpResponse(json.dumps(data),  content_type="application/json")
                except:
                    data['servererror'] = 1
                    messages.success(request,'Sorry, your money transfering process has been failed , due to some server error.Please try again later.')
                    return HttpResponse(json.dumps(data),  content_type="application/json")
        return HttpResponse(json.dumps(data),  content_type="application/json")





@login_required(login_url='Login')
def Myaddress(request):
    context = {}
    context['countries'] = dict(countries)
    return render(request,'users/Myaddress.html', context=context)

@login_required(login_url='Login')
def myaddress(request):
    context = {}
    context['countries'] = dict(countries)
    return render(request,'users/address.html', context=context)


def editaddress(request):
    if request.method == 'POST':
        data = {}
        country = request.POST['country']
        state = request.POST['state']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']

        if state.replace(' ', '').isalpha() and city.replace(' ', '').isalpha() and pincode.isnumeric():
            code = 'IN'
            for i in list(countries):
                if i[1] ==  country:
                    code = i[0]
                    break
            userdetail = usersdetails.objects.filter(users = request.user).first()
            userdetail.country = code
            userdetail.address1 = address
            userdetail.city = city
            userdetail.state = state
            userdetail.pincode = pincode
            userdetail.addresstatus = 1
            userdetail.save()
            data['valid'] = 1
            messages.success(request, 'Your Address has been updated successfully.')
            return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            if state.replace(' ', '').isalpha() != True:
                data['staterror'] = 1
            if pincode.isnumeric() != True:
                data['pincode'] = 1
            if city.replace(' ', '').isalpha() != True:
                data['cityerror'] = 1

            return HttpResponse(json.dumps(data),  content_type="application/json")


def resetpassword(request):
    context = {}
    return render(request,'users/resetpassword.html', context=context)


def postoresetpassword(request):
    if request.method == 'POST':
        data = {}
        email = request.POST['email']
        user = User.objects.filter(email=email).first()
        if user != None:
            sendresettoken(email, user.first_name)
            messages.success(request, 'Please check your email Inbox, A Password Reset link has been send for reseting password.')
            data['valid'] = 1
            return HttpResponse(json.dumps(data),  content_type="application/json")
        else:
            data['nouser'] = 1
            return HttpResponse(json.dumps(data),  content_type="application/json")

def resetmypassword(request, token):
    s = serializer(SECRET_KEY)
    try:
        email = s.loads(token)['email']
        context = {}
        if request.method == 'POST':
            password = request.POST['password']
            user = User.objects.filter(email=email).first()
            user.set_password(password)
            user.save()
            messages.success(request, 'Your Account Password has Reseted successfully.' )
            login(request, user)
            return redirect('home')
        context['email'] = email
        return render(request, 'users/resetmypassword.html', context=context)
    except:
        messages.success(request, 'Your Password Reset  link is expired please generate New one.')
        return redirect('home')
    