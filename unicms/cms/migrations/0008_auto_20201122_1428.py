# Generated by Django 3.1.2 on 2020-11-22 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0007_auto_20201118_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='draft_of',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='type',
            field=models.CharField(choices=[('standard', 'Standard Page'), ('home', 'Home Page')], default='standard', max_length=33),
        ),
    ]