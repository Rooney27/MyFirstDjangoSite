# Generated by Django 3.2.6 on 2021-08-17 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0006_auto_20210817_1834'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='count',
        ),
        migrations.AddField(
            model_name='order',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
