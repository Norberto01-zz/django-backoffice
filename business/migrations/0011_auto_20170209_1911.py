# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-09 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_auto_20170131_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='updated_at',
            field=models.DateField(default=django.utils.timezone.now, null=True),
        ),
    ]
