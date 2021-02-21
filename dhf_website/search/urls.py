from django.urls import path
from search.views import home, search, autocomplete_series, autocomplete_character

urlpatterns = [
    path('', home, name='home'),
    path('search', search, name='search'),
    path('autocomplete/series', autocomplete_series, name='autocomplete_series'),
    path('autocomplete/character', autocomplete_character, name='autocomplete_character')
]
