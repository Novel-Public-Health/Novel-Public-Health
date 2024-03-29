# Generated by Django 3.1.2 on 2021-03-26 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0051_delete_movieinstance'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='imdb',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_link',
            field=models.CharField(blank=True, help_text='Can be left blank. Grabbed from imdb links. For example, <a target="_blank" href="https://www.imdb.com/title/tt3322364/">Concussion\'s</a> id is 3322364', max_length=10, verbose_name='IMDB id'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.ForeignKey(blank=True, help_text='Can be left blank. This field will be overwritten if given a valid IMDB id.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.genre'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=models.ForeignKey(help_text='Can be left blank. This field will be overwritten if given a valid IMDB id.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='summary',
            field=models.TextField(help_text='Enter a brief description of the movie.', max_length=1000),
        ),
        migrations.AlterField(
            model_name='movie',
            name='year',
            field=models.CharField(blank=True, help_text='Can be left blank. This field will be overwritten if given a valid IMDB id.', max_length=200, null=True),
        ),
    ]
