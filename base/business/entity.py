##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2018 Université catholique de Louvain (http://www.uclouvain.be)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    A copy of this license - GNU General Public License - is available
#    at the root of the source code of this program.  If not,
#    see http://www.gnu.org/licenses/.
#
##############################################################################
from base import models as mdl
from base.models import entity_calendar, entity_version
from base.models.academic_year import find_academic_year_by_year
from base.models.enums import entity_container_year_link_type, academic_calendar_type
from django.utils import timezone


def get_entities_ids(requirement_entity_acronym, with_entity_subordinated):
    entities_ids = set()
    entity_versions = mdl.entity_version.search(acronym=requirement_entity_acronym)
    entities_ids |= set(entity_versions.values_list('entity', flat=True).distinct())

    if with_entity_subordinated:
        for an_entity_version in entity_versions:
            all_descendants = entity_version.find_descendants(an_entity_version.start_date)
            entities_ids |= {descendant.entity.id for descendant in all_descendants}
    return list(entities_ids)


def get_entity_container_list(entities_id_list_param, entity_ids, entity_container_yr_link_type):
    entities_id_list = entities_id_list_param
    entities_id_list += list(
        mdl.entity_container_year.search(
            link_type=entity_container_yr_link_type,
            entity_id=entity_ids
        ).values_list(
            'learning_container_year', flat=True
        ).distinct()
    )
    return entities_id_list


def get_entity_calendar(an_entity_version, academic_yr):
    entity_cal = entity_calendar.find_by_entity_and_reference_for_current_academic_year(
        an_entity_version.entity.id, academic_calendar_type.SUMMARY_COURSE_SUBMISSION)
    if entity_cal is None:
        if an_entity_version.parent:
            parent_entity_version = entity_version.find_latest_version_by_entity(an_entity_version.parent,
                                                                                 timezone.now())
            return get_entity_calendar(parent_entity_version, academic_yr)
        else:
            an_academic_calendar = find_academic_year_by_year(academic_yr.year)
            if an_academic_calendar:
                return an_academic_calendar
    else:
        return entity_cal
