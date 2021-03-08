# Generated by Django 3.1.2 on 2021-03-08 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0041_remove_movie_imdb_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='imdb',
            field=models.CharField(default='', help_text='grabbed from imdb links', max_length=10),
            preserve_default=False,
        ),
    ]
