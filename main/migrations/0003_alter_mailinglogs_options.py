# Generated by Django 4.2.3 on 2023-08-29 14:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_client_photo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailinglogs',
            options={'verbose_name': 'Лог', 'verbose_name_plural': 'Логи'},
        ),
    ]
