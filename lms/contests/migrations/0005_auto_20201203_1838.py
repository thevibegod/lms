# Generated by Django 3.1.3 on 2020-12-03 18:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0004_auto_20201203_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='options/'),
        ),
        migrations.AlterField(
            model_name='question',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='questions/'),
        ),
    ]
