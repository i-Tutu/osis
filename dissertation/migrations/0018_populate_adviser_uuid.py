# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-26 12:56
from __future__ import unicode_literals

from django.db import migrations
import uuid
from dissertation.models.adviser import Adviser


def populate_adviser_uuid(apps, schema_editor):
    adviser_ids = Adviser.objects.values_list('id',flat=True)
    for id in adviser_ids:
        Adviser.objects.filter(pk=id).update(uuid=uuid.uuid4())


class Migration(migrations.Migration):
    dependencies = [
        ('dissertation', '0017_add_adviser_uuid'),
    ]

    operations = [
        migrations.RunPython(populate_adviser_uuid),
    ]