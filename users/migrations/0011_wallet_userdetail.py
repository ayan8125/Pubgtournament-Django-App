# Generated by Django 2.2.5 on 2020-08-26 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_remove_wallet_usersdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='userdetail',
            field=models.ForeignKey(default='user1', on_delete=django.db.models.deletion.CASCADE, to='users.usersdetails'),
        ),
    ]
