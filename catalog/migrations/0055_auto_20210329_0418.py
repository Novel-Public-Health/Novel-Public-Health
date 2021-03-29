# Generated by Django 3.1.2 on 2021-03-29 08:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0054_auto_20210326_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='director',
            field=models.ForeignKey(blank=True, help_text='This field will be overwritten                                                                                                 if given a valid IMDB id and left blank.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.director'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='found_articles',
            field=models.TextField(blank=True, help_text='HTML list output of found research                                                                                     articles on Google Scholar. Clear the text to find new articles.', max_length=5000, null=True, verbose_name='Found Research Articles'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(blank=True, help_text='This field will be overwritten if given                                                                                                         a valid IMDB id and left blank.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='summary',
            field=models.TextField(blank=True, help_text='Enter a brief description of the movie. This field will                                                                                     be overwritten if given a valid IMDB id and left blank.', max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='title',
            field=models.CharField(blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(blank=True, help_text='This field will be overwritten if given a valid IMDB id and left blank.', max_length=200, null=True),
        ),
    ]