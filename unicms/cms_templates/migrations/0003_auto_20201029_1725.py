# Generated by Django 3.1.2 on 2020-10-29 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_templates', '0002_auto_20201029_1713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetemplate',
            name='blocks',
            field=models.ManyToManyField(to='cms_templates.PageBlockTemplate'),
        ),
    ]