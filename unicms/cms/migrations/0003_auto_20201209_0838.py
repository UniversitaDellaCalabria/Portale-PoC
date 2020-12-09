# Generated by Django 3.1.2 on 2020-12-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_auto_20201202_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='type',
            field=models.CharField(choices=[('standard', 'Page'), ('home', 'Home Page')], default='standard', max_length=33),
        ),
        migrations.AlterField(
            model_name='publicationlocalization',
            name='content',
            field=models.TextField(blank=True, help_text='Content', null=True),
        ),
    ]