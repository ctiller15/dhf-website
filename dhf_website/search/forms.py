from django import forms

class SearchForm(forms.Form):
    search_term = forms.CharField(
        label="Character Name", 
        max_length=100, 
        required=True,                          
        widget=forms.TextInput(attrs={'required': 'true'}))
