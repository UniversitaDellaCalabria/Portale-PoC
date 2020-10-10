# Generated by Django 3.1.2 on 2020-10-10 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cms_pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('name', models.CharField(blank=True, max_length=160, null=True)),
                ('template_file', models.CharField(choices=[], max_length=1024)),
                ('note', models.TextField(blank=True, help_text='Editorial Board Notes, not visible by public.', null=True)),
            ],
            options={
                'verbose_name_plural': 'Page Templates',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PageTemplateThirdPartyBlock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('section', models.CharField(blank=True, choices=[('pre-head', 'Pre-Header'), ('head', 'Header'), ('menu', 'Navigation Menu'), ('menu-2', 'Navigation Menu 2'), ('menu-3', 'Navigation Menu 3'), ('slider', 'Carousel/Slider'), ('slider-2', 'Carousel/Slider 2'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('pre-footer', 'Pre-Footer'), ('footer', 'Footer')], help_text='Specify the container section in the template where this block would be rendered.', max_length=33, null=True)),
                ('block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_pages.pageblock')),
                ('template', models.ForeignKey(limit_choices_to={'is_active': True}, on_delete=django.db.models.deletion.CASCADE, to='cms_templates.pagetemplate')),
            ],
            options={
                'verbose_name_plural': 'Page Template Third-Party Blocks',
            },
        ),
        migrations.CreateModel(
            name='PageBlockTemplate',
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
                ('template_file', models.CharField(choices=[], default='base.html', max_length=1024)),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_templates.pagetemplate')),
            ],
            options={
                'verbose_name_plural': 'Page Block HTML Templates',
                'ordering': ['name'],
            },
        ),
    ]