# Generated by Django 3.1.2 on 2020-10-06 08:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms_context', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EditorialBoardEditors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('permission', models.CharField(choices=[('0', 'everything everywhere'), ('1', 'can edit created by him/her'), ('2', 'can edit all pages in his/her context'), ('3', 'can edit all pages in his/her context and descendants'), ('3', 'can edit all pages'), ('4', 'can edit his/her own'), ('5', 'can translate all pages in his/her context'), ('6', 'can translate all pages in his/her context and descendants'), ('7', 'can translate all pages'), ('8', 'can publish created by him/her'), ('9', 'can publish all pages in his/her context'), ('10', 'can publish all pages in his/her context and descendants'), ('11', 'can publish all pages')], max_length=5)),
                ('is_active', models.BooleanField()),
                ('context', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms_context.editorialboardcontext')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'EditorialBoard Context Users',
            },
        ),
        migrations.RemoveField(
            model_name='editorialboardusers',
            name='context',
        ),
        migrations.RemoveField(
            model_name='editorialboardusers',
            name='role',
        ),
        migrations.RemoveField(
            model_name='editorialboardusers',
            name='user',
        ),
        migrations.DeleteModel(
            name='EditorialBoardRolePermissions',
        ),
        migrations.DeleteModel(
            name='EditorialBoardUsers',
        ),
    ]
