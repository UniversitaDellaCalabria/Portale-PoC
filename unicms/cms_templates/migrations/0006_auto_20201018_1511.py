# Generated by Django 3.1.2 on 2020-10-18 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_templates', '0005_auto_20201018_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetemplate',
            name='blocks',
            field=models.ManyToManyField(blank=True, null=True, to='cms_templates.PageBlockTemplate'),
        ),
    ]
