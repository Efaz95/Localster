# Generated by Django 3.0.7 on 2020-06-24 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200624_1814'),
    ]

    operations = [
        migrations.AlterField(
            model_name='influencer',
            name='ig_url',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
