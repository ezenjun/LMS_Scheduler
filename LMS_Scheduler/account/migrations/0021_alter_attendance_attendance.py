# Generated by Django 3.2.3 on 2021-08-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_attendance_attendance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='attendance',
            field=models.DateTimeField(),
        ),
    ]
