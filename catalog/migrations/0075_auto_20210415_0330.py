# Generated by Django 3.1.2 on 2021-04-15 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0074_auto_20210415_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_type',
            field=models.IntegerField(choices=[(1, 'free - access independent films and media outlets'), (2, 'Low Subscription - access to Hollywood films'), (3, 'Premium Subscription - access to A-list movies')], default=1, verbose_name='Subscription Tier'),
        ),
    ]