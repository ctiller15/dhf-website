from django import forms
from django.utils.safestring import mark_safe

class RelationForm(forms.Form):
    character_name = forms.CharField(label='Character', max_length=200)
    summary = forms.CharField(label='summary', max_length=500, widget=forms.Textarea())
    character_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

class ReferenceForm(forms.Form):
    title = forms.CharField(max_length=200, label=False)

class CharacterCreationForm(forms.Form):
    CHOICES = (( 1, 'Yes'), ( 2, 'No'), ( 3,'Maybe'),)
    thumbnail = forms.ImageField(label='Character Image', required=False, widget=forms.ClearableFileInput(attrs = {
        'onchange': "previewImage(this);"
    }))
    character_name = forms.CharField(label='Character Name', max_length=200, min_length=0)
    character_id = forms.CharField(required=False, widget=forms.HiddenInput(attrs={'readonly': 'readonly'}))
    character_series = forms.CharField(label='Character Series', max_length=200, min_length=0)
    character_series_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    f_status = forms.ChoiceField(label=mark_safe("<br />Do they fuck?"), choices=CHOICES)
    summary = forms.CharField(label=mark_safe('<br />Summary'), widget=forms.Textarea(), max_length=500, required=False)
