# Generated by Django 3.2.3 on 2021-07-28 08:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_alter_statistics_daily'),
    ]

    operations = [
        migrations.RenameField(
            model_name='priority',
            old_name='rank',
            new_name='usertype',
        ),
        migrations.RemoveField(
            model_name='priority',
            name='myclass',
        ),
    ]
