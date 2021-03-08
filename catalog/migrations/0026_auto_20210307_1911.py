# Generated by Django 3.1.2 on 2021-03-08 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0025_auto_20210307_1858'),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('summary', models.TextField(help_text='Enter a brief description of the movie', max_length=1000)),
                ('isbn', models.CharField(help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=13, unique=True, verbose_name='ISBN')),
                ('director', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.director')),
            ],
            options={
                'ordering': ['title', 'director'],
            },
        ),
        migrations.CreateModel(
            name='MovieInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular movie across whole library', primary_key=True, serialize=False)),
                ('imprint', models.CharField(max_length=200)),
                ('due_back', models.DateField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('d', 'Maintenance'), ('o', 'On loan'), ('a', 'Available'), ('r', 'Reserved')], default='d', help_text='Movie availability', max_length=1)),
                ('borrower', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='catalog.movie')),
            ],
            options={
                'ordering': ['due_back'],
                'permissions': (('can_mark_returned', 'Set movie as returned'),),
            },
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='book',
        ),
        migrations.RemoveField(
            model_name='bookinstance',
            name='borrower',
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(help_text='Enter a movie genre (e.g. Science Fiction, French Poetry etc.)', max_length=200),
        ),
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text="Enter the movie's natural language (e.g. English, French, Japanese etc.)", max_length=200),
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='BookInstance',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.ManyToManyField(help_text='Select a genre for this movie', to='catalog.Genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.language'),
        ),
    ]
