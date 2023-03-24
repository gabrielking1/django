# Generated by Django 3.2.18 on 2023-03-24 22:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('supervisor', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=125)),
                ('year', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1895), django.core.validators.MaxValueValidator(2050)])),
                ('level', models.CharField(choices=[('ND', 'Nd'), ('HND', 'Hnd')], max_length=4)),
                ('date', models.DateField(auto_now=True)),
                ('file', models.FileField(upload_to='documents/')),
                ('source_code', models.FileField(upload_to='source/')),
                ('name', models.CharField(max_length=124)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.department')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.faculty')),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='faculty',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='persons.faculty'),
        ),
    ]