# Generated by Django 3.1.2 on 2021-03-08 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0039_auto_20210308_0133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(help_text='grabbed from imdb links', max_length=10),
        ),
    ]
