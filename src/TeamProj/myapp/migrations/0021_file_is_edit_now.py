# Generated by Django 3.1 on 2020-08-14 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0020_auto_20200813_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='is_edit_now',
            field=models.BooleanField(default=False, verbose_name='是否正在被编辑'),
        ),
    ]
