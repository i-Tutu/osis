##############################################################################
#
#    OSIS stands for Open Student Information System. It's an application
#    designed to manage the core business of higher education institutions,
#    such as universities, faculties, institutes and professional schools.
#    The core business involves the administration of students, teachers,
#    courses, programs and so on.
#
#    Copyright (C) 2015-2017 Université catholique de Louvain (http://www.uclouvain.be)
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
from django.db import models
from osis_common.models.serializable_model import SerializableModel, SerializableModelAdmin
from base.models.enums import learning_unit_year_subtypes, learning_container_year_types, internship_subtypes, \
    learning_unit_year_session, entity_type
from base.models import entity_container_year as mdl_entity_container_year
from base.models import entity_version as mdl_entity_version

from base.models.enums import entity_container_year_link_type

class LearningUnitYearAdmin(SerializableModelAdmin):
    list_display = ('external_id', 'acronym', 'title', 'academic_year', 'credits', 'changed', 'structure', 'status')
    fieldsets = ((None, {'fields': ('academic_year', 'learning_unit', 'acronym', 'title', 'title_english', 'credits',
                                    'decimal_scores', 'structure', 'learning_container_year',
                                    'subtype', 'status', 'internship_subtype', 'session')}),)
    list_filter = ('academic_year', 'vacant', 'in_charge', 'decimal_scores')
    raw_id_fields = ('learning_unit', 'learning_container_year', 'structure')
    search_fields = ['acronym', 'structure__acronym', 'external_id']


class LearningUnitYear(SerializableModel):
    external_id = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.ForeignKey('AcademicYear')
    learning_unit = models.ForeignKey('LearningUnit')
    learning_container_year = models.ForeignKey('LearningContainerYear', blank=True, null=True)
    changed = models.DateTimeField(null=True, auto_now=True)
    acronym = models.CharField(max_length=15, db_index=True)
    title = models.CharField(max_length=255)
    title_english = models.CharField(max_length=250, blank=True, null=True)
    subtype = models.CharField(max_length=50, blank=True, null=True,
                               choices=learning_unit_year_subtypes.LEARNING_UNIT_YEAR_SUBTYPES)
    credits = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    decimal_scores = models.BooleanField(default=False)
    team = models.BooleanField(default=False)
    vacant = models.BooleanField(default=False)
    in_charge = models.BooleanField(default=False)
    structure = models.ForeignKey('Structure', blank=True, null=True)
    internship_subtype = models.CharField(max_length=50, blank=True, null=True,
                               choices=internship_subtypes.INTERNSHIP_SUBTYPES)
    status = models.BooleanField(default=False)
    session = models.CharField(max_length=50, blank=True, null=True,
                               choices=learning_unit_year_session.LEARNING_UNIT_YEAR_SESSION)

    def __str__(self):
        return u"%s - %s" % (self.academic_year, self.acronym)

    @property
    def subdivision(self):
        if self.acronym and self.learning_container_year:
            return self.acronym.replace(self.learning_container_year.acronym, "")
        return None

    @property
    def parent(self):
        if self.subdivision:
            return LearningUnitYear.objects.filter(
                subtype=learning_unit_year_subtypes.FULL,
                learning_container_year=self.learning_container_year,
                learning_container_year__acronym=self.learning_container_year.acronym,
                learning_container_year__container_type=learning_container_year_types.COURSE
            ).first()
        return None

    @property
    def same_container_learning_unit_years(self):
        return LearningUnitYear.objects.filter(
            learning_container_year=self.learning_container_year
        ).order_by('acronym')

    @property
    def is_service_course(self):
        return is_service_course(self)
        # faculty_ref = None
        #
        # entity_container_yr = mdl_entity_container_year.find_requirement_entity2(self.learning_container_year)
        # if entity_container_yr:
        #     if entity_container_yr.entity:
        #         entity_version = mdl_entity_version.get_last_version(entity_container_yr.entity)
        #         faculty_ref = entity_version.entity
        #         if entity_version:
        #             if entity_version.entity_type == entity_type.FACULTY:
        #                 faculty_ref = entity_version.entity
        #             else:
        #                 f = check_parent(entity_version.parent)
        #                 if f:
        #                     faculty_ref= f
        #
        #
        #
        # return faculty_ref
    # @property
    # def get_parent_faculty_version(self):
    #     print(self.learning_container_year.id)
    #     entity_container_yr = mdl_entity_container_year.find_by_learning_container_year(self.learning_container_year,
    #                                                                                     entity_container_year_link_type.REQUIREMENT_ENTITY)
    #
    #     if entity_container_yr:
    #         entity_version = mdl_entity_version.get_last_version(parent_entity)
    #         return mdl_entity_version.find_parent_faculty_version(entity_version, self.academic_year)
    #
    #     return None

def check_parent(parent_entity):
    entity_version = mdl_entity_version.get_last_version(parent_entity)

    if entity_version:
        if entity_version.entity_type == entity_type.FACULTY:
            return entity_version.entity
        else:
            return check_parent(entity_version.parent)
    return None



def find_by_id(learning_unit_year_id):
    return LearningUnitYear.objects.select_related('learning_container_year__learning_container')\
                                   .get(pk=learning_unit_year_id)


def find_by_acronym(acronym):
    return LearningUnitYear.objects.filter(acronym=acronym)\
                                   .select_related('learning_container_year')


def search(academic_year_id=None, acronym=None, learning_container_year_id=None, learning_unit=None,
           title=None, subtype=None, status=None, container_type=None, *args, **kwargs):
    queryset = LearningUnitYear.objects

    if academic_year_id:
        queryset = queryset.filter(academic_year=academic_year_id)

    if acronym:
        queryset = queryset.filter(acronym__icontains=acronym)

    if learning_container_year_id is not None:
        if isinstance(learning_container_year_id, list):
            queryset = queryset.filter(learning_container_year__in=learning_container_year_id)
        elif learning_container_year_id:
            queryset = queryset.filter(learning_container_year=learning_container_year_id)

    if learning_unit:
        queryset = queryset.filter(learning_unit=learning_unit)

    if title:
        queryset = queryset.filter(title__icontains=title)

    if subtype:
        queryset = queryset.filter(subtype=subtype)

    if status:
        queryset = queryset.filter(status=status)

    if container_type:
        queryset = queryset.filter(learning_container_year__container_type=container_type)

    return queryset.select_related('learning_container_year')


def find_gte_year_acronym(academic_yr, acronym):
    return LearningUnitYear.objects.filter(academic_year__year__gte=academic_yr.year,
                                           acronym__iexact=acronym)


def find_lt_year_acronym(academic_yr, acronym):
    return LearningUnitYear.objects.filter(academic_year__year__lt=academic_yr.year,
                                           acronym__iexact=acronym).order_by('academic_year')

def is_service_course(learning_unit_yr):
    print('is_service_course')
    print(learning_unit_yr.entities)

    entity_version = learning_unit_yr.entities['REQUIREMENT_ENTITY']
    entity_container_yr = mdl_entity_container_year.find_requirement_entity(learning_unit_yr.learning_container_year)

    enti = mdl_entity_version.find_parent_faculty_version(entity_version,
                                                          learning_unit_yr.learning_container_year)

    if enti is None:
        enti = entity_container_yr.entity
    else:
        enti = enti.entity
    enti_v = mdl_entity_version.get_last_version(enti)
    entity_allocation = mdl_entity_container_year.find_allocation_entity(learning_unit_yr.learning_container_year)
    entity_allocation_v = mdl_entity_version.get_last_version(entity_allocation.entity)
    for e in enti_v.find_descendants(learning_unit_yr.academic_year.start_date):
        if e == entity_allocation_v:

            return False
    return True

