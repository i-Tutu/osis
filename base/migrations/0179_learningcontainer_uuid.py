# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-03 13:24
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0178_auto_20171031_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningcontainer',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, null=True),
        ),
    ]