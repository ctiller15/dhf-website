from characters.models import Character
from django.shortcuts import render

def handle_character_list(request):
    if request.method == 'GET':
        characters = Character.objects.all().order_by('name')

        return render(request, 'character_list_page.html', context={ 'results': characters })

