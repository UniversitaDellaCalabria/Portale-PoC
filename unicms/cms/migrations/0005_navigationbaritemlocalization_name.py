# Generated by Django 3.1.2 on 2020-10-29 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0004_navigationbaritemlocalization'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationbaritemlocalization',
            name='name',
            field=models.CharField(default='value', max_length=33),
            preserve_default=False,
        ),
    ]