# Generated by Django 3.2.6 on 2021-09-02 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0014_rename_discont_item_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotionitem',
            name='largeImage',
            field=models.ImageField(default='static/items/foto/no_foto.jpg', upload_to='static/items/Promofoto'),
        ),
        migrations.AddField(
            model_name='promotionitem',
            name='smallImage',
            field=models.ImageField(default='static/items/foto/no_foto.jpg', upload_to='static/items/Promofoto'),
        ),
    ]
