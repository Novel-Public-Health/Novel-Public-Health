# Generated by Django 3.1.2 on 2021-03-08 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0040_auto_20210308_0133'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='imdb_id',
        ),
    ]
