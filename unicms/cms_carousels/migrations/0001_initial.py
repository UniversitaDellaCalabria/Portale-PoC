# Generated by Django 3.1.2 on 2020-12-02 16:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField()),
                ('name', models.CharField(max_length=160)),
                ('description', models.TextField(max_length=2048)),
            ],
            options={
                'verbose_name_plural': 'Carousels',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='CarouselItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('pre_heading', models.CharField(blank=True, help_text='Pre Heading', max_length=120, null=True)),
                ('heading', models.CharField(blank=True, help_text='Heading', max_length=120, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('carousel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_carousels.carousel')),
            ],
            options={
                'verbose_name_plural': 'Carousel Items',
            },
        ),
        migrations.CreateModel(
            name='CarouselItemLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('title_preset', models.CharField(choices=[('view', 'View'), ('open', 'Open'), ('read more', 'Read More'), ('more', 'More'), ('get in', 'Get in'), ('enter', 'Enter'), ('submit', 'Submit'), ('custom', 'custom')], default='custom', max_length=33)),
                ('title', models.CharField(blank=True, help_text='Title', max_length=120, null=True)),
                ('url', models.CharField(max_length=2048)),
                ('carousel_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_carousels.carouselitem')),
            ],
            options={
                'verbose_name_plural': 'Carousel Item Links',
            },
        ),
        migrations.CreateModel(
            name='CarouselItemLocalization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('order', models.IntegerField(blank=True, default=10, null=True)),
                ('is_active', models.BooleanField()),
                ('language', models.CharField(choices=[('ar', 'Arabic'), ('en', 'English'), ('es', 'Spanish'), ('fr', 'French'), ('it', 'Italian'), ('pt', 'Portuguese')], default='en', max_length=12)),
                ('pre_heading', models.CharField(blank=True, help_text='Pre Heading', max_length=120, null=True)),
                ('heading', models.CharField(blank=True, help_text='Heading', max_length=120, null=True)),
                ('description', models.TextField(blank=True, null=True)),
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
                ('order', models.IntegerField(blank=True, default=10, null=True)),
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
