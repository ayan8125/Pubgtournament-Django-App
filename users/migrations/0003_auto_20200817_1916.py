# Generated by Django 2.2.5 on 2020-08-17 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usersphone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersphone',
            name='phnumber1',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='usersphone',
            name='phnumber2',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]