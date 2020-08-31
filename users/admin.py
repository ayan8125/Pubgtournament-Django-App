from django.contrib import admin
from .models import user,wallet, redem, usersdetails, mymessages
# Register your models here.

admin.site.register(user)
admin.site.register(usersdetails)
admin.site.register(wallet)
admin.site.register(redem)
admin.site.register(mymessages)