# Generated by Django 3.2.3 on 2021-07-28 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0017_qna_qna_view'),
    ]

    operations = [
        migrations.AddField(
            model_name='notices',
            name='notice_view',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
