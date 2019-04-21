from django import forms
from django.forms import ModelForm
from api.models import DegreeModel, SubplanModel


class EditProgramFormSnippet(ModelForm):

    class Meta:
        model = DegreeModel
        fields = ('code', 'year', 'name', 'units', 'degreeType', 'studentNotes')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text"}),
            'year': forms.TextInput(attrs={'class': "text"}),
            'name': forms.TextInput(attrs={'class': "text"}),
            'units': forms.TextInput(attrs={'class': "text"}),
        }
        labels = {
            'studentNotes': "Student Notes",
            'degreeType': "Program Type"
        }


class StaffNotesFormSnippet(ModelForm):
    class Meta:
        model = DegreeModel
        fields = ('staffNotes',)
        labels = {
            'staffNotes': "Staff Notes"
        }


class EditSubplanFormSnippet(ModelForm):
    class Meta:
        model = SubplanModel
        fields = ('code', 'year', 'name', 'units', 'planType')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text"}),
            'year': forms.TextInput(attrs={'class': "text"}),
            'name': forms.TextInput(attrs={'class': "text"}),
            'units': forms.TextInput(attrs={'class': "text"}),
        }
