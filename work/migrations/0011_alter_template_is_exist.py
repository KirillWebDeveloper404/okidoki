# Generated by Django 3.2.8 on 2022-01-29 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0010_template_is_exist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='is_exist',
            field=models.BooleanField(blank=True, default=True, verbose_name='удаление'),
        ),
    ]