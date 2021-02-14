from django.urls import path
from search.views import home, search, autocomplete_series

urlpatterns = [
    path('', home, name='home'),
    path('search', search, name='search'),
    path('autocomplete/series', autocomplete_series, name='autocomplete_series')
]
