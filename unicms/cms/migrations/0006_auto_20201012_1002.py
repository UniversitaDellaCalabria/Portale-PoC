# Generated by Django 3.1.2 on 2020-10-12 10:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_context', '0001_initial'),
        ('cms', '0005_publicationlocalization_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='navigationbaritem',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='page_path', to='cms_context.webpath'),
        ),
        migrations.AddField(
            model_name='navigationbaritem',
            name='publication',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pub', to='cms.publication'),
        ),
    ]