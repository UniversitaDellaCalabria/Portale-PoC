# Generated by Django 3.1.2 on 2020-11-18 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_templates', '0006_auto_20201118_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='templateblock',
            name='order',
        ),
    ]
