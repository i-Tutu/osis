# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-30 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0196_auto_20171128_1442'),
    ]

    operations = [
        migrations.AddField(
            model_name='educationgrouplanguage',
            name='changed',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='educationgrouplanguage',
            name='external_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]