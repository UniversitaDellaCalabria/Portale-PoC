# Generated by Django 3.1.2 on 2020-10-30 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0004_auto_20201029_1753'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='section',
            field=models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True),
        ),
    ]
