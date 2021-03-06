# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 19:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quote', '0004_auto_20161126_1831'),
        ('tile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='static//uploads/')),
                ('quote', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='quote.Quote')),
                ('template', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tile.Template')),
            ],
        ),
    ]
