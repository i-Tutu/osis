# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-17 08:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('cms', '0010_auto_20180327_1513'),
    ]

    operations = [
        # Remove translated text related to learning achievements
        migrations.RunSQL("""
            DELETE FROM cms_translatedtext
            WHERE text_label_id in (
                SELECT id
                FROM cms_textlabel
                WHERE label = 'skills_to_be_acquired' AND entity = 'learning_unit_year'
            )
        """),
        # Remove translated text label related to learning achievements
        migrations.RunSQL("""
            DELETE FROM cms_translatedtextlabel
            WHERE text_label_id in (
                SELECT id
                FROM cms_textlabel
                WHERE label = 'skills_to_be_acquired' AND entity = 'learning_unit_year'
            )
        """),
        # Remove text label related to learning achievements
        migrations.RunSQL("""
            DELETE FROM cms_textlabel
            WHERE label = 'skills_to_be_acquired' AND entity = 'learning_unit_year'
        """)
    ]
