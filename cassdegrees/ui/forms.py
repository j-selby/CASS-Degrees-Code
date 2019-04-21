from django import forms
from django.forms import ModelForm
from api.models import DegreeModel, SubplanModel


class EditProgramFormSnippet(ModelForm):

    class Meta:
        model = DegreeModel
        fields = ('code', 'year', 'name', 'units', 'degreeType', 'staffNotes', 'studentNotes')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text"}),
            'year': forms.TextInput(attrs={'class': "text"}),
            'name': forms.TextInput(attrs={'class': "text"}),
            'units': forms.TextInput(attrs={'class': "text"}),
            # 'staffNotes': forms.TextInput(attrs={'class': "text"}),
            # 'studentNotes': forms.TextInput(attrs={'class': "text"}),
        }
#         'disabled': True


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
