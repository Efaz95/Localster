# Generated by Django 3.0.7 on 2020-07-16 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_messages_is_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='hire',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
