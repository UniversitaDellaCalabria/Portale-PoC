# Generated by Django 3.1.2 on 2020-12-10 15:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmstemplates', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagetemplate',
            name='template_file',
            field=models.CharField(choices=[('dipartimento_home_v3_dimes.html', 'dipartimento_home_v3_dimes.html'), ('publication_list.html', 'publication_list.html'), ('publication_view_hero_original.html', 'publication_view_hero_original.html'), ('publication_view.html', 'publication_view.html'), ('portale_home_v_original.html', 'portale_home_v_original.html'), ('two_columns.html', 'two_columns.html'), ('portale_home_v3.html', 'portale_home_v3.html'), ('dipartimento_home_v3.html', 'dipartimento_home_v3.html')], max_length=1024),
        ),
    ]