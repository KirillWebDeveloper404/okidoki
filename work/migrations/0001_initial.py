# Generated by Django 3.2.8 on 2021-12-26 12:46

from django.db import migrations, models
import work.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to=work.models.content_file_name, verbose_name='Шаблон')),
            ],
        ),
    ]
