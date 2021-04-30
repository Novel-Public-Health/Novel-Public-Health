# Generated by Django 3.1.2 on 2021-04-29 17:39

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('catalog', '0083_auto_20210427_1812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]