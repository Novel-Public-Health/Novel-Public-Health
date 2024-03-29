# Generated by Django 3.1.2 on 2021-04-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0076_movie_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='thumbnail',
            field=models.CharField(blank=True, help_text='This field will be overwritten                                                                                                 if given a valid IMDB id and left blank.', max_length=500, null=True, verbose_name='Thumbnail'),
        ),
    ]
