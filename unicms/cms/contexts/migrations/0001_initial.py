# Generated by Django 3.1.2 on 2020-12-09 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=254)),
                ('domain', models.CharField(max_length=254)),
                ('is_active', models.BooleanField(blank=True, default=False)),
            ],
            options={
                'verbose_name_plural': 'Sites',
            },
        ),
        migrations.CreateModel(
            name='WebPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=254)),
                ('alias_url', models.TextField(blank=True, max_length=2048, null=True)),
                ('path', models.TextField(max_length=2048)),
                ('fullpath', models.TextField(blank=True, help_text='final path prefixed with the parent path', max_length=2048, null=True)),
                ('is_active', models.BooleanField()),
                ('alias', models.ForeignKey(blank=True, help_text='Alias that would be redirected to ...', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='alias_path', to='cmscontexts.webpath')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpath_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='webpath_modified_by', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, help_text='path be prefixed with the parent one, on save', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='related_path', to='cmscontexts.webpath')),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cmscontexts.website')),
            ],
            options={
                'verbose_name_plural': 'Site Contexts (WebPaths)',
            },
        ),
        migrations.CreateModel(
            name='EditorialBoardLocks',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('locked_time', models.DateTimeField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cmscontexts_editorialboardlocks_locked_items', to='contenttypes.contenttype', verbose_name='content type')),
                ('locked_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Editorial Board Locks',
                'ordering': ('-locked_time',),
            },
        ),
        migrations.CreateModel(
            name='EditorialBoardEditors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('permission', models.CharField(choices=[('1', 'can edit created by him/her in his/her context'), ('2', 'can edit all pages in his/her context'), ('3', 'can edit all pages in his/her context and descendants'), ('4', 'can translate all pages in his/her context'), ('5', 'can translate all pages in his/her context and descendants'), ('6', 'can publish created by him/her in his/her context'), ('7', 'can publish all pages in his/her context'), ('8', 'can publish all pages in his/her context and descendants')], max_length=5)),
                ('is_active', models.BooleanField()),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editorialboardeditors_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='editorialboardeditors_modified_by', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('webpath', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cmscontexts.webpath')),
            ],
            options={
                'verbose_name_plural': 'Editorial Board Users',
            },
        ),
    ]