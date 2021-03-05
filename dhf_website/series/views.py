from django.shortcuts import render
# Move model over to series app.
from characters.models import Series, Character

dictionary_status_map = {
    1: 'Fucks',
    2: 'Possibly Fucks',
    3: 'Do Not Fucks',
}

def series_list(request):
    if request.method == 'GET':
        series_list = Series.objects.all().order_by('name')

        return render(request, 'series_list.html', context={ 'results': series_list })

def series_characters(request, series_id):
    if request.method == 'GET':

        series_name = Series.objects.get(id=series_id).name
        character_list = Character.objects.filter(series__id=series_id).order_by('name').values()

        for item in character_list:
            item.update( {'f_status_string': dictionary_status_map[item['f_status_id']]})

        return render(request, 'series_characters.html', context={ 'results': character_list, 'series_name': series_name })

