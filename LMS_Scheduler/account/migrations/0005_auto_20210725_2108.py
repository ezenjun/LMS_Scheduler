# Generated by Django 3.2.3 on 2021-07-25 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_faq'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='faq',
            name='faq_date',
        ),
        migrations.RemoveField(
            model_name='faq',
            name='faq_no',
        ),
    ]