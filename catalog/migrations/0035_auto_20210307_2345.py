# Generated by Django 3.1.2 on 2021-03-08 04:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0034_remove_movie_movie_genre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(blank=True, help_text='Select a genre for this movie', to='catalog.Genre'),
        ),
    ]
