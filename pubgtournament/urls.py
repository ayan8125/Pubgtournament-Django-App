"""pubgtournament URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tournaments import views as views1
from users import views as views2 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views1.home,name='home'),
    path('test/', views1.test, name='test'),
    path('Login/', views2.Login, name='Login'),
    path('Signup/', views2.Signup, name='Signup'),
    path('login/', views2.logins, name='login'),
    path('Logout/', views2.Logout, name='Logout'),
    path('signup/', views2.signup, name='signup'),
    path('otp/', views2.otp, name='otp'),
    path('setPassword/', views2.setPassword, name='setPassword'),
    path('uservalidation/<str:token>/', views2.uservalidation, name='uservalidation'),

    path('regestrations/game=<str:game>/tour=<str:tour>/', views1.Regestrations, name='Regestrations'),
    path('regestration/regestrationid=<str:regestrationid>/', views1.Regestrationprox, name='Regestrationprox'),
    path('regestration/handlepayment/<str:response>/',views1.handlepayment,name='handlepayment'),
    path('CancelRegestration/<str:regestrationid>/', views1.CancelRegestration, name='CancelRegestration'),


    path('myadmin/',include('myadmin.urls')),

    path('mymatch/', views2.mymatch, name='mymatch'),
    path('Account/', views2.Account, name='Account'),
    path('user/editname/',views2.editname, name='editname'),
    path('user/editmail/',views2.editmail, name='editmail'),
    path('emailreset/<str:token>/',views2.emailreset, name='emailreset'),
    path('user/editpassword/',views2.editpassword, name='editpassword'),
    path('user/editnumber/',views2.editnumber, name='editnumber'),
    path('user/checkotp/',views2.checkotp, name='checkotp'),
    path('user/setprofileimage/' ,views2.setprofileimage, name='setprofileimage'),
    path('Myaddress/', views2.Myaddress, name='Myaddress'),
    path('myaddress/', views2.myaddress, name='myaddress'),
    path('user/editaddress/', views2.editaddress, name='editaddress'),
    path('resetpassword/', views2.resetpassword, name='resetpassword'),
    path('postoresetpassword/', views2.postoresetpassword, name='postoresetpassword'),
    path('resetmypassword/<str:token>/', views2.resetmypassword, name='resetmypassword'),
    path('redemymoney/',views2.redemymoney, name='redemymoney'),
    path('posttoredemmoney/', views2.posttoredemmoney, name='posttoredemmoney'),
    
    path('usernotification/', views1.usernotification, name='usernotification'),


    path('tournaments/',views1.pasttournaments, name='pasttournaments' ),


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
