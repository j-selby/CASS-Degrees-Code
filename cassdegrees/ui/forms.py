from django import forms
from django.forms import ModelForm
from api.models import DegreeModel, SubplanModel


class EditProgramFormSnippet(ModelForm):

    class Meta:
        model = DegreeModel
        fields = ('code', 'year', 'name', 'units', 'degreeType')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text tfull"}),
            'year': forms.TextInput(attrs={'class': "text tfull"}),
            'name': forms.TextInput(attrs={'class': "text tfull"}),
            'units': forms.TextInput(attrs={'class': "text tfull"}),
        }
        labels = {
            'degreeType': "Program Type",
        }


class StaffNotesFormSnippet(ModelForm):
    class Meta:
        model = DegreeModel
        fields = ('staffNotes',)
        labels = {
            'staffNotes': "Staff Notes"
        }
        widgets = {
            'staffNotes': forms.Textarea(attrs={'class': "tfull"}),
        }


class ProgramContentSnippet(ModelForm):
    class Meta:
        model = DegreeModel
        fields = ('studentNotes',)
        labels = {
            'studentNotes': "Student Notes",
        }
        widgets = {
            'studentNotes': forms.Textarea(attrs={'class': "tfull"}),
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


# TODO: UPDATE WHEN COURSE INTERACTION FOR SUBPLANS IS DEVELOPED
class SubplanContentSnippet(ModelForm):
    class Meta:
        model = SubplanModel
        fields = ('courses',)
        labels = {
            'courses': "PLACEHOLDER CONTENT",
        }
        widgets = {
            # 'studentNotes': forms.Textarea(attrs={'class': "tfull"}),
        }
