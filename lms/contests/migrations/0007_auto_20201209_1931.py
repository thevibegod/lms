# Generated by Django 3.1.3 on 2020-12-09 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0006_totalscore_final_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalscore',
            name='final_section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contests.section'),
        ),
    ]