from django.db.models import F
from django.forms.models import model_to_dict
from django.shortcuts import render
from characters.models import Character, CharacterRelation, CharacterReference
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from characters.forms import CharacterCreationForm, ReferenceForm, RelationForm
from django.forms import formset_factory

def calculate_f_status_text(input_text):
    statuses = {
        'yes': 'fucks',
        'no': 'DOES NOT fuck',
        'maybe': 'MIGHT fuck'
    }

    return statuses[input_text]

@login_required
def character_creation_page(request):
    RelationsFormSet = formset_factory(RelationForm)
    ReferencesFormSet = formset_factory(ReferenceForm)
    if request.method == 'GET':
        form = CharacterCreationForm()

        context = {
            'form': form,
            'relations_form': RelationsFormSet(prefix='relations-form'),
            'references_form': ReferencesFormSet(prefix='references-form'),
        }

        return render(request, 'character_creation_page.html', context=context)
    elif request.method == 'POST':
        character_creation_form = CharacterCreationForm(request.POST)
        # save character
        print(request.POST)
        relations_formset = RelationsFormSet(request.POST, prefix='relations-form')
        references_formset = ReferencesFormSet(request.POST, prefix='references-form')

        print(character_creation_form)
        print(character_creation_form.cleaned_data)
        print(relations_formset)
        print(relations_formset.cleaned_data)
        print(references_formset.cleaned_data)

def character_page(request, character_name):
    if request.method == 'GET':

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

        references = CharacterReference.objects \
            .filter(character=character['id']) \
            .values('text')

        context = {
            'name': character['name'],
            'f_status_text': calculate_f_status_text(character['f_status__name']),
            'f_status': character['f_status__name'],
            'series': character['series__name'],
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
