from django.db import models
from django.utils import timezone
from users.models import user
from game.models import Game
from django.contrib.auth.models import User
# Create your models here.

choices = ((0,'pending'),(1,'Done'),(2,'Canceled'),(3,'started'))
gamechoices = ((0, 'Single Player'),(1, 'Duo Players'), (2, '4 Players(Squad)'))

class tournaments(models.Model):
    tourid = models.IntegerField(primary_key=True,auto_created=True)
    tourname = models.CharField(max_length = 100,blank=True,default='')
    game = models.ForeignKey(Game, on_delete=models.CASCADE,default=1)
    tourdate = models.DateTimeField(default=timezone.now)
    noofplayer = models.IntegerField(default=100)
    tournamenttype = models.IntegerField(default=0, choices = gamechoices)
    availseats = models.IntegerField(default=100)
    occupiedseats = models.IntegerField(default=0)
    entryfee = models.FloatField(default=100.0)
    reward = models.FloatField(default=1000.0)
    roomid = models.CharField(default='', max_length = 255, blank=True)
    roompassword = models.CharField(max_length=255, default= '', blank=True)
    winneremail = models.CharField(max_length=255, default= '', blank=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE)
    tourstatus = models.IntegerField(default=0,choices=choices)


    def __str__(self):
        return f'{self.tourid} {self.tourstatus} {self.availseats} {self.noofplayer}'

    def giveday(self):
        return f'{self.tourdate.strftime("%d")}'

    def fivemonth(self):
        return f'{self.tourdate.strftime("%b")}'

    def givetime(self):
        return f'{self.tourdate.strftime("%I")}'

    def givetimes(self):
        return f'{self.tourdate.strftime("%I")}:{self.tourdate.strftime("%m")} {self.tourdate.strftime("%p")}'

    def giveamorpm(self):
        return f'{self.tourdate.strftime("%p")}'

    def givedate(self):
        return f'{self.tourdate.strftime("%d")} / {self.tourdate.strftime("%b")} / {self.tourdate.strftime("%Y") }'

    def giveyear(self):
        return f'{self.tourdate.strftime("%Y")}'
    
    def givestatus(self):
        keys = self.tourstatus
        for i in choices:
            if i[0] == keys:
                return i[1]
        return ''

    def givemonthdigits(self):
        return int(self.tourdate.strftime("%m")) - 1

    def givehour(self):
        return self.tourdate.strftime("%H")
    
    def giveminutes(self):
        return self.tourdate.strftime("%M")
    
    def giveseconds(self):
        return self.tourdate.strftime("%S")

class regestration(models.Model):
    sid = models.CharField(primary_key=True,max_length=255, default='solo')
    tournament = models.ForeignKey(tournaments,on_delete=models.CASCADE)
    status =  models.IntegerField(default=0, choices = choices)
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    regestrationfee = models.FloatField(default=0.0)
    razorpayorderid = models.CharField(max_length=255,default='',blank=True)
    razorpaymentid = models.CharField(max_length=255,default='',blank=True)
    razorpaysignature = models.CharField(max_length=255,default='',blank=True)


    def __str__(self):
        return f'{self.tournament.tourname} {self.tournament.tourstatus} {self.user.user.first_name}'


    def givedate(self):
        hostingdate = self.tournament.tourdate
        return f"{hostingdate.strftime('%d')} {hostingdate.strftime('%b')}, {hostingdate.strftime('%Y')}"



    def givehourleft(self):
        tdate = timezone.now()
        tourdate = self.tournament.tourdate
        diff = tourdate - tdate
        if tourdate > tdate:
            if int(diff.seconds/3600) == 0:
                return f"{int(diff.seconds/60)} mins left"
            return f"{int(diff.seconds/3600)}, hrs left"
        else:
            if self.tournament.tourstatus == 1:
                return f"Match has Ended"
            if self.tournament.tourstatus == 2:
                return f"Match has Canceled"
            return f"Match has Started"
        