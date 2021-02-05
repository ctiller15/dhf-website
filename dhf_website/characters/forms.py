from django import forms

class RelationForm(forms.Form):
    character_name = forms.CharField(label='Character', max_length=200)
    summary = forms.CharField(label='summary', max_length=500)

class ReferenceForm(forms.Form):
    title = forms.CharField(max_length=200)

class CharacterCreationForm(forms.Form):
    CHOICES = (('Yes', 'Yes'), ('No', 'No'), ('Maybe', 'Maybe'),)
    character_name = forms.CharField(label='Character name', max_length=200)
    character_series = forms.CharField(label='Character Series', max_length=200)
    f_status = forms.ChoiceField(choices=CHOICES)
    summary = forms.CharField(max_length=500)
