from django.urls import path
from series.views import series_list, series_characters

urlpatterns = [
    path('list/', series_list, name='series_list'),
    path('id=<int:series_id>/', series_characters, name='series_characters')
]
