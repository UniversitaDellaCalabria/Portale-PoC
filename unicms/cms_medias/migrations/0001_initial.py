# Generated by Django 3.1.2 on 2020-11-14 17:07

import cms_medias.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('title', models.CharField(blank=True, help_text='Media file title', max_length=60, null=True)),
                ('file', models.FileField(upload_to=cms_medias.models.context_media_path)),
                ('description', models.TextField()),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('file_format', models.CharField(blank=True, choices=[('text/plain', 'text/plain'), ('application/vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.text'), ('application/msword', 'application/msword'), ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), ('text/csv', 'text/csv'), ('application/json', 'application/json'), ('application/vnd.ms-excel', 'application/vnd.ms-excel'), ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), ('application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.spreadsheet'), ('application/wps-office.xls', 'application/wps-office.xls'), ('image/jpeg', 'image/jpeg'), ('image/png', 'image/png'), ('image/gif', 'image/gif'), ('image/x-ms-bmp', 'image/x-ms-bmp'), ('application/pdf', 'application/pdf'), ('application/pkcs7-mime', 'application/pkcs7-mime')], max_length=256, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='media_modified_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Media',
            },
        ),
        migrations.CreateModel(
            name='MediaCollection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(max_length=1024)),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags')),
            ],
            options={
                'verbose_name_plural': 'Media Collections',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MediaCollectionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('collection', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='cms_medias.mediacollection')),
                ('media', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='cms_medias.media')),
            ],
            options={
                'verbose_name_plural': 'Media Collection Items',
                'ordering': ['order'],
            },
        ),
    ]
