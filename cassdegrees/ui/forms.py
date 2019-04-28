import json

from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.forms import ModelForm
from api.models import DegreeModel, SubplanModel
from django.core.exceptions import NON_FIELD_ERRORS

class JSONField(forms.CharField):
    def __init__(self, *args, field_id, **kwargs):
        super().__init__(widget=forms.HiddenInput(attrs={'id': field_id}), *args, **kwargs)

    def to_python(self, value):
        return json.loads(value)


class EditProgramFormSnippet(ModelForm):
    # Use custom handlers for JSON fields
    globalRequirements = JSONField(field_id='globalRequirements', required=False)
    # rules = JSONField(field_id='rules')

    class Meta:
        model = DegreeModel
        fields = ('code', 'year', 'name', 'units', 'degreeType', 'globalRequirements') #, 'rules')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text tfull"}),
            'year': forms.NumberInput(attrs={'class': "text tfull", 'type': "number"}),
            'name': forms.TextInput(attrs={'class': "text tfull"}),
            'units': forms.NumberInput(attrs={'class': "text tfull", 'type': "number"}),
            # DegreeType auto generated
        }
        labels = {
            'degreeType': "Program Type",
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "A program with the same %(field_labels)s already exists!",
            }
        }

    def clean_code(self):
        data = self.cleaned_data['code']
        if len(data) < 4:
            raise forms.ValidationError("This should be at least 4 characters!")
        return data

    def clean_year(self):
        data = self.cleaned_data['year']
        if data < 2000 or data > 3000:
            raise forms.ValidationError("This should be between 2000-3000!")
        return data

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 5:
            raise forms.ValidationError("This should be at least 5 characters!")
        return data


class EditSubplanFormSnippet(ModelForm):
    # Automatically injected by default
    units = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = SubplanModel
        fields = ('code', 'year', 'name', 'units', 'planType')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text tfull"}),
            'year': forms.NumberInput(attrs={'class': "text tfull", 'type': "number"}),
            'name': forms.TextInput(attrs={'class': "text tfull"}),
            # See units above
            # planType auto generated
        }
        labels = {
            'planType': "Plan Type",
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "A plan with the same %(field_labels)s already exists!",
            }
        }

    def clean_code(self):
        data = self.cleaned_data['code']
        if len(data) < 4:
            raise forms.ValidationError("This should be at least 4 characters!")
        return data

    def clean_year(self):
        data = self.cleaned_data['year']
        if data < 2000 or data > 3000:
            raise forms.ValidationError("This should be between 2000-3000!")
        return data

    def clean_name(self):
        data = self.cleaned_data['name']
        if len(data) < 5:
            raise forms.ValidationError("This should be at least 5 characters!")
        return data

    def clean_units(self):
        # Generate units from subtype plan selected
        subplanUnits = \
            {
                'MAJ': 48,
                'MIN': 24,
                'SPEC': 24
            }

        return subplanUnits[self.data["planType"]]


# class StaffNotesFormSnippet(ModelForm):
#     class Meta:
#         model = DegreeModel
#         fields = ('staffNotes',)
#         labels = {
#             'staffNotes': "Staff Notes"
#         }
#         widgets = {
#             'staffNotes': forms.Textarea(attrs={
#                 'class': "tfull",
#                 'placeholder': "Notes for other CASS staff - these will not be displayed on the final template"}),
#         }
#
#
# class ProgramContentSnippet(ModelForm):
#     class Meta:
#         model = DegreeModel
#         fields = ('studentNotes',)
#         labels = {
#             'studentNotes': "Student Notes",
#             'globalRequirements': "Global Requirements"
#         }
#         widgets = {
#             'studentNotes': forms.Textarea(attrs={
#                 'class': "tfull",
#                 'placeholder': "Explanatory program notes for students - these will be displayed on the final template"
#             }
#             ),
#         }
#
#
# class EditSubplanFormSnippet(ModelForm):
#     class Meta:
#         model = SubplanModel
#         fields = ('code', 'year', 'name', 'units', 'planType')
#         widgets = {
#             'code': forms.TextInput(attrs={'class': "text tfull"}),
#             'year': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
#             'name': forms.TextInput(attrs={'class': "text tfull"}),
#             'units': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
#         }
#
#
# # TODO: UPDATE WHEN COURSE INTERACTION FOR SUBPLANS IS DEVELOPED
# class SubplanContentSnippet(ModelForm):
#     class Meta:
#         model = SubplanModel
#         fields = ('courses',)
#         labels = {
#             'courses': "PLACEHOLDER CONTENT",
#         }
#         widgets = {
#             # 'studentNotes': forms.Textarea(attrs={'class': "tfull"}),
#         }
