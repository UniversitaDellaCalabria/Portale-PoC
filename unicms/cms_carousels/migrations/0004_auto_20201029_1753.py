# Generated by Django 3.1.2 on 2020-10-29 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0003_auto_20201029_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='carouselitemlinklocalization',
            name='order',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
        migrations.AddField(
            model_name='carouselitemlocalization',
            name='order',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]