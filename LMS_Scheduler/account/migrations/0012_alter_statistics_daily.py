# Generated by Django 3.2.3 on 2021-07-27 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_alter_statistics_daily'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statistics',
            name='daily',
            field=models.TimeField(),
        ),
    ]
