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
from django import forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from waffle.decorators import waffle_flag

from base.forms.education_group.common import EducationGroupModelForm
from base.forms.education_group.group import GroupForm
from base.forms.education_group.mini_training import MiniTrainingForm
from base.forms.education_group.training import TrainingForm
from base.models.education_group_type import EducationGroupType, find_authorized_types
from base.models.education_group_year import EducationGroupYear
from base.models.enums import education_group_categories
from base.views import layout
from base.views.common import display_success_messages
from base.views.common_classes import FlagMixin, AjaxTemplateMixin
from base.views.education_groups.perms import can_create_education_group


class EducationGroupTypeForm(forms.Form):
    name = forms.ModelChoiceField(EducationGroupType.objects.none(), label=_("training_type"), required=True)

    def __init__(self, parent, category, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["name"].queryset = find_authorized_types(
            category=category,
            parents=parent
        )


class SelectEducationGroupTypeView(FlagMixin, AjaxTemplateMixin, FormView):
    flag = "education_group_create"
    # rules = [can_create_education_group]
    # raise_exception = True
    template_name = "education_group/blocks/form/education_group_type.html"
    form_class = EducationGroupTypeForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["category"] = self.kwargs["category"]
        kwargs["parent"] = get_object_or_404(
            EducationGroupYear, pk=self.kwargs["parent_id"]
        ) if self.kwargs.get("parent_id") else None
        return kwargs

    def form_valid(self, form):
        # Attach form to the object to use it in get_success_url
        self.form = form
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(create_education_group, kwargs=self.kwargs) + \
               "?education_group_type=" + \
               str(self.form.cleaned_data["name"].pk)


@login_required
@waffle_flag("education_group_create")
@can_create_education_group
def create_education_group(request, category, parent_id=None):
    parent = get_object_or_404(EducationGroupYear, id=parent_id) if parent_id is not None else None
    education_group_type = get_object_or_404(EducationGroupType, pk=request.GET.get("education_group_type"))

    forms_by_category = {
        education_group_categories.GROUP: GroupForm,
        education_group_categories.TRAINING: TrainingForm,
        education_group_categories.MINI_TRAINING: MiniTrainingForm,
    }

    form_education_group_year = forms_by_category[category](
        request.POST or None,
        parent=parent,
        education_group_type=education_group_type
    )

    if form_education_group_year.is_valid():
        education_group_year = form_education_group_year.save()

        parent_id = parent.pk if parent else education_group_year.pk

        success_msg = create_success_message_for_creation_education_group_year(parent_id, education_group_year)
        display_success_messages(request, success_msg, extra_tags='safe')

        url = reverse("education_group_read", args=[parent_id, education_group_year.pk])

        return redirect(url)

    templates_by_category = {
        education_group_categories.GROUP: "education_group/create_groups.html",
        education_group_categories.TRAINING: "education_group/create_trainings.html",
        education_group_categories.MINI_TRAINING: "education_group/create_mini_trainings.html",
    }

    return layout.render(request, templates_by_category.get(category), {
        "form_education_group_year": form_education_group_year.forms[forms.ModelForm],
        "form_education_group": form_education_group_year.forms[EducationGroupModelForm],
        "parent": parent
    })


def create_success_message_for_creation_education_group_year(parent_id, education_group_year):
    MSG_KEY = "Education group year <a href='%(link)s'> %(acronym)s (%(academic_year)s) </a> successfuly created."
    link = reverse("education_group_read", args=[parent_id, education_group_year.id])
    return _(MSG_KEY) % {"link": link, "acronym": education_group_year.acronym,
                         "academic_year": education_group_year.academic_year}
