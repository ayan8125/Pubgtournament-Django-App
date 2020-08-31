from django.urls import path, include
from myadmin import views as views1

urlpatterns = [
    path('',views1.MyADMIN,name='MyADMIN'),
    path('adminlogin/',views1.adminlogin, name='adminlogin'),
    path('adminlogout/', views1.adminlogout,name='adminlogout'),
    path('adminregister/', views1.adminregister, name='adminregister'),
    path('admin/emailvalidation/<str:token>/', views1.adminemailvalidation, name='adminemailvalidation'),

    path('admin/sendcredentails/', views1.sendcredentails, name='sendcredentails'),
    path('admin/sendcredentailsemail/', views1.send_credentails_email, name='sendcredentailsemail'),
    path('admin/canceltour/', views1.canceltour, name='canceltour'),
    path('admin/starttour/', views1.canceltour, name='starttour'),
    path('admin/completetour/', views1.canceltour, name='completetour'),

    path('activetournaments/', views1.activetournaments, name='activetournaments'),
    path('completetournaments/', views1.completetournaments, name='completetournaments'),
    path('tournament/<str:tourid>/', views1.DetailsOfTournament, name='DetailsOfTournament'),
    path('tournaments/makewinner/', views1.makewinner, name='makewinner'),
    path('tournament/schedule/<str:tourid>/', views1.tournament, name='tournament'),

]