# Generated by Django 3.1 on 2020-08-13 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_file_delete_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_content',
            field=models.TextField(null=True, verbose_name='文档内容'),
        ),
    ]
