# Generated by Django 3.1.2 on 2021-03-29 08:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0057_auto_20210329_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='max_num_find_articles',
            field=models.IntegerField(blank=True, default=5, help_text='Default number is 5.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)], verbose_name='Max number of research articles'),
        ),
    ]
