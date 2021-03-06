# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-10-17 10:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0368_auto_20181017_1142'),
    ]

    operations = [
        migrations.AlterField(
            model_name='educationgroupyear',
            name='diploma_printing_title',
            field=models.CharField(blank=True, default='', max_length=140, verbose_name='diploma_title'),
        ),
        migrations.AlterField(
            model_name='educationgroupyear',
            name='joint_diploma',
            field=models.BooleanField(default=False, verbose_name='university_certificate_desc'),
        ),
        migrations.AlterField(
            model_name='educationgroupyear',
            name='professional_title',
            field=models.CharField(blank=True, default='', max_length=320, verbose_name='professionnal_title'),
        ),
    ]
