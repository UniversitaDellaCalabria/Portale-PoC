# Generated by Django 3.1.2 on 2020-11-20 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_contexts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='webpath',
            name='alias',
            field=models.ForeignKey(blank=True, help_text='Alias that would be redirected to ...', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alias_path', to='cms_contexts.webpath'),
        ),
    ]
