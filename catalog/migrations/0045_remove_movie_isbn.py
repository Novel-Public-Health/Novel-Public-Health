# Generated by Django 3.1.2 on 2021-03-23 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0044_auto_20210323_0509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='isbn',
        ),
    ]
