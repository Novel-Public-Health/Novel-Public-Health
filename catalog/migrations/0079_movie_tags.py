# Generated by Django 3.1.2 on 2021-04-27 03:14

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('catalog', '0078_auto_20210419_0519'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
