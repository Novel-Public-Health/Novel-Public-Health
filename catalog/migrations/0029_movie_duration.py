# Generated by Django 3.1.2 on 2021-03-08 02:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0028_auto_20210307_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='duration',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]
