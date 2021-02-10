from django.db.models import F
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from characters.models import Character, CharacterRelation, CharacterReference, F_Status, Series, CharacterReference
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
        relations_formset = RelationsFormSet(request.POST, prefix='relations-form')
        references_formset = ReferencesFormSet(request.POST, prefix='references-form')
        print("Found it!!!")
            
        if(request.user.is_authenticated and character_creation_form.is_valid()):

            cleaned_character = character_creation_form.cleaned_data
            print(cleaned_character)
            # Only run if series id is not given.
            char_series = Series.objects.create(name=cleaned_character['character_series'])
            found_f_status=F_Status.objects.get(id=cleaned_character['f_status'])
            print(found_f_status)

            new_character = Character.objects.create(
                name=cleaned_character['character_name'],
                summary=cleaned_character['summary'],
                f_status=found_f_status,
                series=char_series,
            )

            for relation in relations_formset.cleaned_data:
                char_relation = Character.objects.create(
                    name=relation['character_name'],
                    f_status=found_f_status,
                    series=char_series,
                )

                relation_obj = CharacterRelation.objects.create(character_1=new_character, character_2=char_relation, relation_summary=relation['summary'])

            for reference in references_formset.cleaned_data:
                CharacterReference.objects.create(character=new_character, text=reference['title'])

            return redirect(f'/characters/char-id-{new_character.id}/')

        else:
            # convert to a class override?
            # Or simply redirect to the login page.
            return HttpResponse('Unauthorized', status=401)

def character_page(request, character_name=None, character_id=None):
    if request.method == 'GET':

        character = None

        if character_name:
            character = Character.objects \
                .filter(name=character_name) \
                .values('id', 'name', 'f_status__name', 'series__name') \
                .first()
        elif character_id:
            character = Character.objects \
                .filter(id=character_id) \
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
