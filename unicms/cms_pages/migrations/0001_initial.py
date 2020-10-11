# Generated by Django 3.1.2 on 2020-10-11 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
                ('name', models.CharField(blank=True, help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('schema', models.TextField(choices=[('{}', 'heading'), ('{}', 'body')])),
                ('content', models.TextField(blank=True, help_text='according to the block template schema', null=True)),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu', 'Navigation Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=60, null=True)),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_pages.page')),
            ],
            options={
                'verbose_name_plural': 'Page Block',
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
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu', 'Navigation Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer')], help_text='Specify the container section in the template where this block will be rendered.', max_length=60, null=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_pages.pageblock')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_pages.page')),
            ],
            options={
                'verbose_name_plural': 'Page Third-Party Block',
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
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent_page', to='cms_pages.page')),
                ('related_page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_page', to='cms_pages.page')),
            ],
            options={
                'verbose_name_plural': 'Related Pages',
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
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_pages.page')),
            ],
            options={
                'verbose_name_plural': 'Page Links',
            },
        ),
    ]
