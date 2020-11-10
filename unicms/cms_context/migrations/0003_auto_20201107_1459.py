# Generated by Django 3.1.2 on 2020-11-07 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_context', '0002_auto_20201107_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webpath',
            name='fullpath',
            field=models.TextField(blank=True, help_text='final path prefixed with the parent path', max_length=2048, null=True),
        ),
    ]