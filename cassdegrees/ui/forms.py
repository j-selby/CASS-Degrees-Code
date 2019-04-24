from django import forms
from django.forms import ModelForm
from api.models import DegreeModel, SubplanModel


class EditProgramFormSnippet(ModelForm):
    class Meta:
        model = DegreeModel
        fields = ('code', 'year', 'name', 'units', 'degreeType')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text tfull"}),
            'year': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
            'name': forms.TextInput(attrs={'class': "text tfull"}),
            'units': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
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
            'staffNotes': forms.Textarea(attrs={
                'class': "tfull",
                'placeholder': "Notes for other CASS staff - these will not be displayed on the final template"}),
        }


class ProgramContentSnippet(ModelForm):
    class Meta:
        model = DegreeModel
        fields = ('studentNotes',)
        labels = {
            'studentNotes': "Student Notes",
            'globalRequirements': "Global Requirements"
        }
        widgets = {
            'studentNotes': forms.Textarea(attrs={
                'class': "tfull",
                'placeholder': "Explanatory program notes for students - these will be displayed on the final template"
            }
            ),
        }


class EditSubplanFormSnippet(ModelForm):
    class Meta:
        model = SubplanModel
        fields = ('code', 'year', 'name', 'units', 'planType', 'published')
        widgets = {
            'code': forms.TextInput(attrs={'class': "text tfull"}),
            'year': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
            'name': forms.TextInput(attrs={'class': "text tfull"}),
            'units': forms.TextInput(attrs={'class': "text tfull", 'type': "number"}),
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
