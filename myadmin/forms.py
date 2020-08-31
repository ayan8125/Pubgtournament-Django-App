from django.forms import ModelForm
from tournaments.models import tournaments



class Tournamentform(ModelForm):
    class Meta:
        model = tournaments
        fields = '__all__'