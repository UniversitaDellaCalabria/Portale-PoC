# Generated by Django 3.1.2 on 2020-10-30 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0006_remove_carousel_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carouselitemlocalization',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]