# Generated by Django 3.1.2 on 2020-11-09 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_medias', '0003_delete_medialink'),
        ('cms', '0012_publicationcontext_section'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms_medias.mediacollection')),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cms.publication')),
            ],
            options={
                'verbose_name_plural': 'Publication Image Gallery',
            },
        ),
    ]