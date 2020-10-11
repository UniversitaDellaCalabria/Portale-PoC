# Generated by Django 3.1.2 on 2020-10-11 22:15

from django.conf import settings
import django.contrib.sites.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WebSite',
            fields=[
                ('site_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sites.site')),
                ('is_active', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Sites',
            },
            bases=('sites.site',),
            managers=[
                ('objects', django.contrib.sites.models.SiteManager()),
            ],
        ),
        migrations.CreateModel(
            name='WebPath',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=254)),
                ('path', models.TextField(max_length=2048)),
                ('is_active', models.BooleanField()),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_context.website')),
            ],
            options={
                'verbose_name_plural': 'Site Contexts (WebPaths)',
            },
        ),
        migrations.CreateModel(
            name='EditorialBoardEditors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('permission', models.CharField(choices=[('1', 'can edit created by him/her'), ('2', 'can edit all pages in his/her context'), ('3', 'can edit all pages in his/her context and descendants'), ('4', 'can translate all pages in his/her context'), ('5', 'can translate all pages in his/her context and descendants'), ('6', 'can publish created by him/her'), ('7', 'can publish all pages in his/her context'), ('8', 'can publish all pages in his/her context and descendants')], max_length=5)),
                ('is_active', models.BooleanField()),
                ('context', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms_context.webpath')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Editorial Board Users',
            },
        ),
    ]
