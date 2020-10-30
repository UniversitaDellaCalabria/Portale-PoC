# Generated by Django 3.1.2 on 2020-10-30 13:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms_context', '0001_initial'),
        ('cms', '0009_auto_20201030_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publication',
            name='context',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='in_evidence_end',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='in_evidence_start',
        ),
        migrations.CreateModel(
            name='PublicationContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('in_evidence_start', models.DateTimeField(blank=True, null=True)),
                ('in_evidence_end', models.DateTimeField(blank=True, null=True)),
                ('context', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_context.webpath')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contpub_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contpub_modified_by', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.publication')),
            ],
            options={
                'verbose_name_plural': 'Publication Contexts',
            },
        ),
    ]
