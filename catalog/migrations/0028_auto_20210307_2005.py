# Generated by Django 3.1.2 on 2021-03-08 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_movie_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='file',
            field=models.FileField(upload_to='movie-uploads/'),
        ),
    ]
