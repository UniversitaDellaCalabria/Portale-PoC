# Generated by Django 3.1.2 on 2020-11-22 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0009_auto_20201122_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='content_types',
            field=models.CharField(blank=True, choices=[('markdown', 'markdown'), ('html', 'html')], default='markdown', max_length=33, null=True),
        ),
    ]