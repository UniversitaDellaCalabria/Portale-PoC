# Generated by Django 3.1.2 on 2020-11-02 10:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_menus', '0006_remove_navigationbar_context'),
        ('cms', '0010_auto_20201030_1334'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('menu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_menus.navigationbar')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.page')),
            ],
            options={
                'verbose_name_plural': 'Page Navigation Bars',
            },
        ),
    ]
