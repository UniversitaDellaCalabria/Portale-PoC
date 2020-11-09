# Generated by Django 3.1.2 on 2020-11-09 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0013_publicationgallery'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicationgallery',
            name='is_active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicationgallery',
            name='order',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
