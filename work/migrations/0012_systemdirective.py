# Generated by Django 3.2.8 on 2022-02-01 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work', '0011_alter_template_is_exist'),
    ]

    operations = [
        migrations.CreateModel(
            name='SystemDirective',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('desc', models.TextField()),
            ],
            options={
                'verbose_name': 'SystemDirective',
                'verbose_name_plural': 'SystemDirectives',
                'managed': True,
            },
        ),
    ]
