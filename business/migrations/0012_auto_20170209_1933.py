# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-09 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0011_auto_20170209_1911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='transaction_code',
            field=models.CharField(default=0, max_length=20, verbose_name='Transaction Code'),
            preserve_default=False,
        ),
    ]
