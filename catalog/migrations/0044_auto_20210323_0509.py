# Generated by Django 3.1.2 on 2021-03-23 09:09

from django.db import migrations
import s3direct.fields


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0043_auto_20210308_0146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='file',
            field=s3direct.fields.S3DirectField(blank=True),
        ),
    ]
