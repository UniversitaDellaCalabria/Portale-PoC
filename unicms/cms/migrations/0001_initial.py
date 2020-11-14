# Generated by Django 3.1.2 on 2020-11-14 17:07

import cms.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(max_length=1024)),
                ('image', models.ImageField(blank=True, max_length=512, null=True, upload_to='images/categories')),
            ],
            options={
                'verbose_name_plural': 'Content Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('name', models.CharField(max_length=160)),
                ('note', models.TextField(blank=True, help_text='Editorial Board Notes, not visible by public.', null=True)),
                ('date_start', models.DateTimeField()),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('state', models.CharField(choices=[('draft', 'Draft'), ('wait', 'Wait for a revision'), ('published', 'Published')], default='draft', max_length=33)),
                ('type', models.CharField(choices=[('standard', 'Standard Page'), ('custom', 'Custom Page'), ('home', 'Home Page')], default='standard', max_length=33)),
            ],
            options={
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='PageBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('name', models.CharField(blank=True, help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('type', models.TextField(choices=[('cms_templates.blocks.NullBlock', 'Null Block'), ('cms_templates.blocks.HtmlBlock', 'HTML Block'), ('cms_templates.blocks.JSONBlock', 'JSON Block'), ('unical.flescaTeam.custom_blocks.AngularJSONBlock', 'Angular JSON Block')])),
                ('content', models.TextField(blank=True, help_text='according to the block template schema', null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Block',
            },
        ),
        migrations.CreateModel(
            name='PageCarousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Carousel',
            },
        ),
        migrations.CreateModel(
            name='PageLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(help_text='url')),
            ],
            options={
                'verbose_name_plural': 'Page Links',
            },
        ),
        migrations.CreateModel(
            name='PageMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Navigation Bars',
            },
        ),
        migrations.CreateModel(
            name='PageRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Related Pages',
            },
        ),
        migrations.CreateModel(
            name='PageThirdPartyBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block will be rendered.', max_length=60, null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Third-Party Block',
            },
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('title', models.CharField(help_text='Heading, Headline', max_length=256)),
                ('subheading', models.TextField(blank=True, help_text='Strap line (press)', max_length=1024, null=True)),
                ('content', tinymce.models.HTMLField(blank=True, help_text='Content', null=True)),
                ('state', models.CharField(choices=[('draft', 'Draft'), ('wait', 'Wait for a revision'), ('published', 'Published')], default='draft', max_length=33)),
                ('date_start', models.DateTimeField(blank=True, null=True)),
                ('date_end', models.DateTimeField(blank=True, null=True)),
                ('note', models.TextField(blank=True, help_text='Editorial Board notes', null=True)),
                ('slug', models.SlugField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Publications',
            },
        ),
        migrations.CreateModel(
            name='PublicationAttachment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('name', models.CharField(blank=True, help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('file', models.FileField(upload_to=cms.models.context_publication_attachment_path)),
                ('description', models.TextField()),
                ('file_size', models.IntegerField(blank=True, null=True)),
                ('file_format', models.CharField(blank=True, choices=[('text/plain', 'text/plain'), ('application/vnd.oasis.opendocument.text', 'application/vnd.oasis.opendocument.text'), ('application/msword', 'application/msword'), ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'), ('text/csv', 'text/csv'), ('application/json', 'application/json'), ('application/vnd.ms-excel', 'application/vnd.ms-excel'), ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'), ('application/vnd.oasis.opendocument.spreadsheet', 'application/vnd.oasis.opendocument.spreadsheet'), ('application/wps-office.xls', 'application/wps-office.xls'), ('image/jpeg', 'image/jpeg'), ('image/png', 'image/png'), ('image/gif', 'image/gif'), ('image/x-ms-bmp', 'image/x-ms-bmp'), ('application/pdf', 'application/pdf'), ('application/pkcs7-mime', 'application/pkcs7-mime')], max_length=256, null=True)),
            ],
            options={
                'verbose_name_plural': 'Publication Attachments',
            },
        ),
        migrations.CreateModel(
            name='PublicationContext',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu-1', 'Navigation Main Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('menu-4', 'Navigation Menu 4'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer'), ('post-footer', 'Post-Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('in_evidence_start', models.DateTimeField(blank=True, null=True)),
                ('in_evidence_end', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Publication Contexts',
            },
        ),
        migrations.CreateModel(
            name='PublicationGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
            ],
            options={
                'verbose_name_plural': 'Publication Image Gallery',
            },
        ),
        migrations.CreateModel(
            name='PublicationRelated',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_page', to='cms.publication')),
                ('related', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_page', to='cms.publication')),
            ],
            options={
                'verbose_name_plural': 'Related Publications',
            },
        ),
        migrations.CreateModel(
            name='PublicationLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('title', models.CharField(help_text='Heading, Headline', max_length=256)),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('pt', 'Portuguese')], default='en', max_length=12)),
                ('subheading', models.TextField(blank=True, help_text='Strap line (press)', max_length=1024, null=True)),
                ('content', tinymce.models.HTMLField(blank=True, help_text='Content', null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publoc_created_by', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='publoc_modified_by', to=settings.AUTH_USER_MODEL)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.publication')),
            ],
            options={
                'verbose_name_plural': 'Publication Localizations',
            },
        ),
        migrations.CreateModel(
            name='PublicationLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField(help_text='url')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.publication')),
            ],
            options={
                'verbose_name_plural': 'Publication Links',
            },
        ),
    ]
