# Generated by Django 3.1.2 on 2020-10-31 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0007_auto_20201030_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]