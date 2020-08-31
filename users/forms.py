from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from user.models import useraddresses,usersphone,proxyorder
from orders.models import order,slotorder 
from merchant.models import groupsofbook,groupsoflist
# from .models import Profile
CHOICES = [('1', 'HOME(7am to 9pm Deliver)'), ('2', 'OFFICE / COMMERCIAL(10am to 6pm)')]
class setpassword(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Set Username','id':'username','type':'text','class':'input-field'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'set Password','id':'password','type':'password','class':'input-field'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm Password','id':'password2','type':'password','class':'input-field'}))


class Usersignup(UserCreationForm):
    firstname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'firstname','id':'name','type':'text','class':'input-field'}))
    lastname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last name','id':'lastname','type':'text','class':'input-field'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email','id':'email1','name':'email1','type':'email','class':'input-field'}))
    phnumber = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ph-no','id':'phnumber','type':'number','class':'input-field'}))

    class Meta:
        model = User
        fields = ['firstname','lastname','email']


# class userprofile(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = ['userimage','country','phone','phone2']




class userdetails(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name'] 



class otpform(forms.Form):
    otp = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '','id':'otp','type':'text','class':'input-field'}))
  

class addressform(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'fullname','id':'fullname','type':'text','class':'input-field'}))
    mobileno = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '10 digit mobile Number ,enter without using prefix(+91 or 0)','id':'mobileno','type':'number','class':'input-field'}))
    pincode = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': '6 digits Pincode','id':'pincode','type':'number','class':'input-field'}))
    houseno = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'houseno/ flatno / Building / floor','id':'houseno','type':'text','class':'input-field'}))
    areaname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'street / locality / Colony ','id':'areaname','type':'text','class':'input-field'}))
    landmmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Eg: Near Poona College of Arts ,Commerce and Science','id':'landmmark','type':'text','class':'input-field'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'city','id':'city','type':'text','class':'input-field'}))
    address_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)


class userdetails(forms.ModelForm):
    class Meta:
        model = useraddresses
        fields = ['addid','fullname','mobileno','pincode','houseno','areaname','landmark','towncity','address_type'] 

    

class userdetails1(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name'] 

class userdetails2(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']



class userdetails3(forms.ModelForm):
    class Meta:
        model = usersphone
        fields = ['phnumber1']

class userdetails4(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']

class changepassword(forms.Form):
    currentpass = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Current Password','id':'currentpass','type':'password','class':'input-field'}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'set Password','id':'password1','type':'password','class':'input-field'}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Confirm Password','id':'password2','type':'password','class':'input-field'}))

class ordersform(forms.ModelForm):
    class Meta:
        model = order
        fields = '__all__'

class proxyordersform(forms.ModelForm):
    class Meta:
        model = proxyorder
        fields = '__all__'

class slotsordersform(forms.ModelForm):
    class Meta:
        model = slotorder
        fields = '__all__'
    
class groupoflistform(forms.ModelForm):
    class Meta:
        model = groupsoflist
        fields = '__all__'

class groupofbookform(forms.ModelForm):
    class Meta:
        model = groupsofbook
        fields = '__all__'