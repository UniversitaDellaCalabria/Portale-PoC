# Generated by Django 3.1.2 on 2020-10-29 17:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_carousels', '0002_auto_20201029_1725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carouselitemlink',
            old_name='carousel',
            new_name='carousel_item',
        ),
        migrations.CreateModel(
            name='CarouselItemLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('pt', 'Portuguese')], default='en', max_length=12)),
                ('pre_heading', models.CharField(blank=True, help_text='Pre Heading', max_length=120, null=True)),
                ('heading', models.CharField(blank=True, help_text='Heading', max_length=120, null=True)),
                ('description', models.TextField()),
                ('carousel_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_carousels.carouselitem')),
            ],
            options={
                'verbose_name_plural': 'Carousel Item Localization',
            },
        ),
        migrations.CreateModel(
            name='CarouselItemLinkLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('pt', 'Portuguese')], default='en', max_length=12)),
                ('title', models.CharField(blank=True, help_text='Title', max_length=120, null=True)),
                ('carousel_item_link', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_carousels.carouselitemlink')),
            ],
            options={
                'verbose_name_plural': 'Carousel Item Links',
            },
        ),
    ]
