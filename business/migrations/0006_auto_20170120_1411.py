# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-20 14:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_auto_20170120_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='TransactionStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='transaction',
            name='status_transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='business.TransactionStatus'),
        ),
    ]
