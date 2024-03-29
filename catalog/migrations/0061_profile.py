# Generated by Django 3.1.2 on 2021-04-08 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('catalog', '0060_auto_20210329_0429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('user_type', models.IntegerField(choices=[(1, 'low-tier'), (2, 'mid-tier'), (3, 'supah-tier'), (4, 'admin')])),
            ],
        ),
    ]
