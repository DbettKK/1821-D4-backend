# Generated by Django 3.1 on 2020-08-17 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0026_auto_20200817_1038'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['msg_time']},
        ),
    ]
