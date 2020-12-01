# Generated by Django 3.1.2 on 2020-12-01 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0012_publicationblock'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='publicationblock',
            options={'verbose_name_plural': 'Publication Page Block'},
        ),
        migrations.AddField(
            model_name='publicationblock',
            name='is_active',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='publicationblock',
            name='order',
            field=models.IntegerField(blank=True, default=10, null=True),
        ),
    ]
