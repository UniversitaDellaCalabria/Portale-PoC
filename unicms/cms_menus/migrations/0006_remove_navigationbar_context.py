# Generated by Django 3.1.2 on 2020-11-02 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_menus', '0005_auto_20201030_1419'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='navigationbar',
            name='context',
        ),
    ]
