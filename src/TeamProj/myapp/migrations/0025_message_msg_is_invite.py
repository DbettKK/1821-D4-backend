# Generated by Django 3.1 on 2020-08-17 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_auto_20200816_1939'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='msg_is_invite',
            field=models.BooleanField(default=False, verbose_name='消息是否已读'),
        ),
    ]
