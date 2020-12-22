# Generated by Django 3.1.3 on 2020-11-30 17:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contests', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalscore',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='section',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.contest'),
        ),
        migrations.AddField(
            model_name='section',
            name='questions',
            field=models.ManyToManyField(to='contests.AttendedQuestion'),
        ),
        migrations.AddField(
            model_name='section',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='question',
            name='contest',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.contest'),
        ),
        migrations.AddField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.question'),
        ),
        migrations.AddField(
            model_name='contest',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
        migrations.AddField(
            model_name='contest',
            name='domains',
            field=models.ManyToManyField(to='contests.Domain'),
        ),
        migrations.AddField(
            model_name='attendedquestion',
            name='option',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.option'),
        ),
        migrations.AddField(
            model_name='attendedquestion',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.question'),
        ),
        migrations.AddField(
            model_name='attendedquestion',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.profile'),
        ),
    ]