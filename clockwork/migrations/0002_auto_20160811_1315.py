# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-11 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clockwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
