# Generated by Django 3.1.2 on 2020-10-30 13:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_templates', '0003_auto_20201029_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageblocktemplate',
            name='content',
        ),
    ]