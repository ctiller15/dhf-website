from django import forms

class RelationForm(forms.Form):
    character_name = forms.CharField(label='Character', max_length=200)
    summary = forms.CharField(label='summary', max_length=500)

class ReferenceForm(forms.Form):
    title = forms.CharField(max_length=200)

class CharacterCreationForm(forms.Form):
    CHOICES = (( 1, 'Yes'), ( 2, 'No'), ( 3,'Maybe'),)
    character_name = forms.CharField(label='Character name', max_length=200, min_length=0)
    character_series = forms.CharField(label='Character Series', max_length=200, min_length=0)
    character_series_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
    f_status = forms.ChoiceField(choices=CHOICES)
    summary = forms.CharField(max_length=500, required=False)
