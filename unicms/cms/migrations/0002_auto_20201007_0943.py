# Generated by Django 3.1.2 on 2020-10-07 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pagetemplate',
            old_name='template',
            new_name='template_file',
        ),
    ]
