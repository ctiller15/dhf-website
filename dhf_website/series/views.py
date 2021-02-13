from django.shortcuts import render
# Move model over to series app.
from characters.models import Series, Character

def series_list(request):
    if request.method == 'GET':
        series_list = Series.objects.all()

        return render(request, 'series_list.html', context={ 'results': series_list })

def series_characters(request, series_id):
    if request.method == 'GET':
        character_list = Character.objects.filter(series__id=series_id)

        return render(request, 'series_characters.html', context={ 'results': character_list })

