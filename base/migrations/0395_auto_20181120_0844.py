# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-11-20 08:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0394_auto_20181119_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examenrollment',
            name='score_draft',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0, message='Les scores doivent être compris entre 0 et 20'), django.core.validators.MaxValueValidator(20, message='Les scores doivent être compris entre 0 et 20')]),
        ),
        migrations.AlterField(
            model_name='examenrollment',
            name='score_final',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0, message='Les scores doivent être compris entre 0 et 20'), django.core.validators.MaxValueValidator(20, message='Les scores doivent être compris entre 0 et 20')]),
        ),
        migrations.AlterField(
            model_name='examenrollment',
            name='score_reencoded',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(0, message='Les scores doivent être compris entre 0 et 20'), django.core.validators.MaxValueValidator(20, message='Les scores doivent être compris entre 0 et 20')]),
        ),
    ]
