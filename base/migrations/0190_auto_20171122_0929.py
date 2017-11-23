# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-22 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0189_groupelementyear'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='learningunit',
            options={'permissions': (('can_access_learningunit', 'Can access learning unit'), ('can_edit_learningunit_pedagogy', 'Can edit learning unit pedagogy'), ('can_edit_learningunit_specification', 'Can edit learning unit specification'), ('can_delete_learningunit', 'Can delete learning unit'), ('can_propose_learningunit', 'Can propose learning unit '), ('can_create_learningunit', 'Can create learning unit'))},
        ),
        migrations.AlterModelOptions(
            name='learningunitcomponent',
            options={},
        ),
        migrations.AlterField(
            model_name='learningunityear',
            name='internship_subtype',
            field=models.CharField(blank=True, choices=[('TEACHING_INTERNSHIP', 'TEACHING_INTERNSHIP'), ('CLINICAL_INTERNSHIP', 'CLINICAL_INTERNSHIP'), ('PROFESSIONAL_INTERNSHIP', 'PROFESSIONAL_INTERNSHIP'), ('RESEARCH_INTERNSHIP', 'RESEARCH_INTERNSHIP')], max_length=250, null=True),
        ),
    ]
