from django.urls import path
from series.views import series_list

urlpatterns = [
    path('list/', series_list, name='series_list')
]
