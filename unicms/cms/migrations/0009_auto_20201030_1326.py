# Generated by Django 3.1.2 on 2020-10-30 13:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0004_auto_20201029_1753'),
        ('cms', '0008_pagecarousel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagecarousel',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pagecarousel',
            name='type',
        ),
        migrations.AddField(
            model_name='pagecarousel',
            name='carousel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='cms_carousels.carousel'),
            preserve_default=False,
        ),
    ]
