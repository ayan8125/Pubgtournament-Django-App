# Generated by Django 2.2.5 on 2020-08-26 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_wallet_userdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersdetails',
            name='addresstatus',
            field=models.IntegerField(choices=[(0, 'Not set'), (1, 'set')], default=0),
        ),
        migrations.AlterField(
            model_name='redem',
            name='redemstatus',
            field=models.IntegerField(choices=[(0, 'Confirm'), (1, 'Pending'), (2, 'failed')], default=0),
        ),
    ]