from django.shortcuts import render
# Move model over to series app.
from characters.models import Series

def series_list(request):
    if request.method == 'GET':
        series_list = Series.objects.all()

        return render(request, 'series_list.html', context={ 'results': series_list })
