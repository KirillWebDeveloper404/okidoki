# Generated by Django 3.2.8 on 2021-12-26 12:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_pasport_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': True, 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
