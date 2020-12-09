# Generated by Django 3.1.2 on 2020-12-09 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms_contexts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorialboardeditors',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editorialboardeditors_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='editorialboardeditors',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editorialboardeditors_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='webpath',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpath_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='webpath',
            name='modified_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpath_modified_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
