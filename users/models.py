from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from game.models import Game
from django_countries.fields import CountryField
from django_countries import countries
# Create your models here.
rchoices = (
(1,'ANDHRA BANK'),(2,'ALLAHABAD  BANK'),(3,'AXIS BANK'),(4,'BANK OF BARODA'),(5,'BANK OF INDIA'),(6,'BANK OF MAHARASHTRA'),
(7,'CENTRAL BANK OF INDIA'),(8,'CANARA BANK'),(9,'CATHOLIC SYRIAN BANK'),(10,'CITI BANK'),(11,'CORPORATION BANK'),(12,'DENA BANK'),
(13,'DHANALAKSHMI BANK'),(14,'FEDERAL BANK')
,(15,'HDFC BANK'),(16,'ICICI BANK'),(17,'INDIAN BANK'),(18,'INDIAN OVERSEAS BANK'),(19,'INDUSIND BANK'),(20,'IDBI BANK'),
(21,'JAMMU AND KASHMIR BANK'),(22,'KARNATAKA BANK'),(23,'KOTAK MAHINDRA BANK'),(24,'ORIENTAL BANK OF COMMERECE'),(25,'PUNJAB NATIONAL BANK'),
(26,'PUNJAB & SIND BANK'),(27,'STANDARD CHARTERED BANK'),(28,'STATE BANK OF BIKANER AND JAIPUR'),(29,'STATE BANK OF INDIA'),(30,'STATE BANK OF HYDERABAD'),
(31,'STATE BANK OF TRAVANCORE'),(32,'SOUTH INDIAN BANK'),(33,'SYNDICATE BANK'),(34,'TAMILNADU MERCANTILE BANK'),(35,'TAMILNADU MERCANTILE BANK'),
(36,'UCO BANK'),(37,'VIJAYA BANK'),(38,'YES BANK')

)
choice3= ((1,'seen'),(0,'Not Seen'))
redemchoice = (
    (1,'Confirm'),(2,'Pending'),(0,'failed')
)

address_choices = ((0,'Not set'), (1, 'set'))

class user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, default='',blank=True)
    email = models.EmailField(max_length=100, blank=True)
    createdat = models.DateTimeField(default=timezone.now)
    games = models.ForeignKey(Game, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.first_name} {self.games.gamename}'



class usersdetails(models.Model):
    uid = models.CharField(auto_created=True,primary_key=True,max_length=225)
    userimage = models.ImageField(upload_to='users', default='default.jpg')
    country = models.TextField(default='IN',choices = list(countries), blank=True)
    state = models.CharField(max_length=255, blank=True, default='')
    address1 = models.CharField(max_length=255, blank=True, default='')
    adddres2 = models.CharField(max_length=255, blank=True, default='')
    city = models.CharField(max_length=255, blank=True, default='')
    pincode = models.CharField(max_length=255, blank=True, default='')
    phnumber1 = models.CharField(max_length=255,blank=True,default='')
    phnumber2 = models.CharField(max_length=255,blank=True,default='')
    addresstatus = models.IntegerField(default=0,choices=address_choices)
    users = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.users.first_name} {self.users.last_name} ph-{self.phnumber1} and ph2-{self.phnumber2}'
    


class wallet(models.Model):
    walletid = models.CharField(primary_key=True,max_length=255)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    userdetail =  models.ForeignKey(usersdetails,on_delete=models.CASCADE,default='user1')
    Balanceamt = models.FloatField(default=0.0)
    bank = models.IntegerField(choices=rchoices,default=0)
    holdername = models.CharField(default='',max_length=255)
    accoutno = models.CharField(default='',max_length=100)
    IFSC = models.CharField(default='',max_length=100)
    lastredem = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return f'{self.user} {self.Balanceamt}'


    def givebankname(self):
        for i in rchoices:
            if i[0] == self.bank:
                return i[1]



class redem(models.Model):
    redemid = models.CharField(primary_key=True,max_length=255)
    redemamt = models.FloatField(default=0.0)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    wallets = models.ForeignKey(wallet,on_delete=models.CASCADE,default='Wallet_1325')
    redemstatus = models.IntegerField(default=1,choices=redemchoice)




    def givestatus(self):
        for i in redemchoice:
            if i[0] == self.redemstatus:
                return i[1]
        return ''



class mymessages(models.Model):
    messageid = models.CharField(max_length=255,primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(default='')
    mdate = models.DateTimeField(default=timezone.now)
    message_status = models.IntegerField(default=0,choices=choice3)


    def __str__(self):
        return f' user = {self.user.first_name} , status ={self.message_status}'

    def givestatus(self):
        for i in choice3:
            if i[0] == self.message_status:
                return i[1]
