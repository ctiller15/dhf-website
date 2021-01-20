from django.db.models import F
from django.forms.models import model_to_dict
from django.shortcuts import render
from characters.models import Character, CharacterRelation


def calculate_f_status_text(input_text):
    statuses = {
        'yes': 'fucks',
        'no': 'DOES NOT fuck',
        'maybe': 'MIGHT fuck'
    }

    return statuses[input_text]

def character_page(request, character_name):
    character = Character.objects \
        .filter(name=character_name) \
        .values('id', 'name', 'f_status__name', 'series__name') \
        .first()

    relations = ( CharacterRelation.objects \
        .filter(character_1__id=character['id']) \
        .values('relation_summary', character_name=F('character_2__name')) ) \
    | (CharacterRelation.objects \
       .filter(character_2__id=character['id']) \
       .values('relation_summary', character_name=F('character_1__name')))

    print(character['f_status__name'])

    print(relations)

    context = {
        'name': character['name'],
        'f_status_text': calculate_f_status_text(character['f_status__name']),
        'f_status': character['f_status__name'],
        'series': character['series__name'],
        'relations': relations
    }

    return render(request, 'character_page.html', context={ 'results': context})
