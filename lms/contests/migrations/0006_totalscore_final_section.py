# Generated by Django 3.1.3 on 2020-12-09 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0005_auto_20201203_1838'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalscore',
            name='final_section',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='contests.section'),
            preserve_default=False,
        ),
    ]
