# Generated by Django 3.1.2 on 2021-04-08 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0061_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'free-user'), (2, 'low-subscription'), (3, 'mid-subscription'), (4, 'high-subscription'), (5, 'admin')]),
        ),
    ]
