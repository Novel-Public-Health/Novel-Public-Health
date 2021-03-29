# Generated by Django 3.1.2 on 2021-03-29 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0056_auto_20210329_0424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='max_num_find_articles',
            field=models.IntegerField(blank=True, default=5, help_text='Default number is 5.', verbose_name='Max number of research articles'),
        ),
    ]