# Generated by Django 3.1.2 on 2021-03-26 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0049_movie_found_articles'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='found_articles',
            field=models.CharField(max_length=5000),
        ),
    ]
