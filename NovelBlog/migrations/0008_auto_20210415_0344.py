# Generated by Django 3.1.2 on 2021-04-15 07:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NovelBlog', '0007_comment'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-date_added']},
        ),
    ]
