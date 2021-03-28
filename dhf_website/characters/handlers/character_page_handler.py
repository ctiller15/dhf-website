from django.db.models import F
from django.http import HttpResponse
from characters.models import Character, CharacterRelation, CharacterReference
from characters.helpers import calculate_f_status_text
from django.shortcuts import render
from django.conf import settings

def handle_character_page(request, character_name=None, character_id=None):
    if request.method == 'GET':

        character = None

        if character_name:
            character = Character.objects \
                .filter(name__iexact=character_name) \
                .values('id', 'thumbnail', 'name', 'f_status__name', 'series__name', 'series__id', 'summary') \
                .first()
        elif character_id:
            character = Character.objects \
                .filter(id=character_id) \
                .values('id', 'thumbnail', 'name', 'f_status__name', 'series__name', 'series__id', 'summary') \
                .first()

        relations = ( CharacterRelation.objects \
            .filter(character_1__id=character['id']) \
            .values('relation_summary', character_name=F('character_2__name'), character_id=F('character_2__id') ) \
            .union(CharacterRelation.objects \
           .filter(character_2__id=character['id']) \
                   .values('relation_summary', character_name=F('character_1__name'), character_id=F('character_1__id'))))

        references = CharacterReference.objects \
            .filter(character=character['id']) \
            .values('text')

        context = {
            'name': character['name'],
            'id': character['id'],
            'thumbnail': request.build_absolute_uri('/').strip("/") + settings.MEDIA_URL + str(character['thumbnail']),
            'f_status_text': calculate_f_status_text(character['f_status__name']),
            'f_status': character['f_status__name'],
            'series': character['series__name'],
            'series_id': character['series__id'],
            'summary': character['summary'],
            'relations': relations,
            'references': references,
        }

        return render(request, 'character_page.html', context={ 'results': context})

    elif request.method == 'POST':

        if(request.user.is_authenticated):
            return HttpResponse('Success', status=200)

        else:
            # convert to a class override?
            # Or simply redirect to the login page.
            return HttpResponse('Unauthorized', status=401)

