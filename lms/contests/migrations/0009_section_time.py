# Generated by Django 3.1.3 on 2020-12-15 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0008_auto_20201209_2108'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='time',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]