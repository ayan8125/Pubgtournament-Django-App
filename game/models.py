from django.db import models
from django.utils import timezone
# Create your models here.

class Game(models.Model):
    gameid = models.IntegerField(primary_key=True, auto_created=True)
    gamename = models.CharField(max_length=255, blank=True, default = '')
    createdat = models.DateTimeField(default= timezone.now)

    def __str__(self):
        return f'{self.gamename}'