# Generated by Django 3.1.2 on 2020-11-20 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_contexts', '0002_webpath_alias'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpath',
            name='alias_url',
            field=models.TextField(blank=True, max_length=2048, null=True),
        ),
    ]
