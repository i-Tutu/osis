# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-30 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0032_auto_20171010_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='offerproposition',
            name='global_email_to_commission',
            field=models.BooleanField(default=False),
        ),
    ]
