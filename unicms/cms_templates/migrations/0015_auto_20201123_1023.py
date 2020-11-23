# Generated by Django 3.1.3 on 2020-11-23 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_templates', '0014_auto_20201122_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetemplate',
            name='template_file',
            field=models.CharField(choices=[('publication_view_hero_original.html', 'publication_view_hero_original.html'), ('dipartimento_home_v3_dimes.html', 'dipartimento_home_v3_dimes.html'), ('publication_view.html', 'publication_view.html'), ('dipartimento_home_v3.html', 'dipartimento_home_v3.html'), ('publication_list_brython.html', 'publication_list_brython.html'), ('home_v_original.html', 'home_v_original.html'), ('publication_list.html', 'publication_list.html'), ('home_v3.html', 'home_v3.html')], max_length=1024),
        ),
    ]