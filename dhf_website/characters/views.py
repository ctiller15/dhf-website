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
            
        if(request.user.is_authenticated and character_creation_form.is_valid()):

            cleaned_character = character_creation_form.cleaned_data
            
            if cleaned_character['character_series_id']:
                char_series, created = Series.objects.get_or_create(id=cleaned_character['character_series_id'])
                if created:
                    char_series.name = cleaned_character['character_series']
            else:
                char_series, created = Series.objects.get_or_create(name=cleaned_character['character_series'])

            found_f_status=F_Status.objects.get(id=cleaned_character['f_status'])

            new_character = Character.objects.create(
                name=cleaned_character['character_name'],
                summary=cleaned_character['summary'],
                f_status=found_f_status,
                series=char_series,
            )

            for relation in relations_formset.cleaned_data:
                if 'character_id' in relation and relation['character_id'] is not None:
                    char_relation = Character.objects.get(id=relation['character_id']) 
                elif 'character_name' in relation:
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
                .values('id', 'name', 'f_status__name', 'series__name', 'summary') \
                .first()
        elif character_id:
            character = Character.objects \
                .filter(id=character_id) \
                .values('id', 'name', 'f_status__name', 'series__name', 'summary') \
                .first()

        relations = ( CharacterRelation.objects \
            .filter(character_1__id=character['id']) \
            .values('relation_summary', character_name=F('character_2__name')) ) \
            .union(CharacterRelation.objects \
           .filter(character_2__id=character['id']) \
                   .values('relation_summary', character_name=F('character_1__name')))

        references = CharacterReference.objects \
            .filter(character=character['id']) \
            .values('text')

        context = {
            'name': character['name'],
            'id': character['id'],
            'f_status_text': calculate_f_status_text(character['f_status__name']),
            'f_status': character['f_status__name'],
            'series': character['series__name'],
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

def character_list(request):
    if request.method == 'GET':
        characters = Character.objects.all()

        return render(request, 'character_list_page.html', context={ 'results': characters })

@login_required
def character_update(request):
    if request.method == 'GET':

        character_id = request.GET.get('character_id')

        character = None

        character = Character.objects \
            .filter(id=character_id) \
            .values('id', 'name', 'f_status__name', 'f_status__id', 'series__id', 'series__name', 'summary') \
            .first()

        relations = ( CharacterRelation.objects \
            .filter(character_1__id=character['id']) \
            .values('relation_summary', character_name=F('character_2__name'), character_id=F('character_2__id')) ) \
            .union(CharacterRelation.objects \
            .filter(character_2__id=character['id']) \
                   .values('relation_summary', character_name=F('character_1__name'), character_id=F('character_1__id')))

        references = CharacterReference.objects \
            .filter(character=character['id']) \
            .values('text')

        print(relations)
        print(len(relations))
        print(references)
        print(len(references))
        RelationsFormSet = formset_factory(RelationForm, extra=0)
        ReferencesFormSet = formset_factory(ReferenceForm, extra=0)

        relations_formset = RelationsFormSet(
            prefix='relations-form',
            initial=[
                {
                    'character_name': relation['character_name'], 
                    'summary': relation['relation_summary'], 
                    'character_id': relation['character_id']
                } for relation in relations
            ]
        )

        references_formset = ReferencesFormSet(
            prefix="references-form",
            initial=[
                {
                    'title': reference['text']
                } for reference in references
            ]
        )

        form = CharacterCreationForm(initial={
            'character_name': character['name'],
            'character_id': character['id'],
            'character_series': character['series__name'],
            'character_series_id': character['series__id'],
            'f_status': character['f_status__id'],
            'summary': character['summary'],
        })

        print(form)
        context = {
            'form': form,
            'relations_form': relations_formset,
            'references_form': references_formset,
            'name': character['name'],
            'id': character['id'],
            'f_status_text': calculate_f_status_text(character['f_status__name']),
            'f_status': character['f_status__name'],
            'series': character['series__name'],
            'summary': character['summary'],
            'relations': relations,
            'references': references,
        }

        return render(request, 'character_update_page.html', context={ 'results': context })
    elif request.method == 'POST':
        RelationsFormSet = formset_factory(RelationForm)
        ReferencesFormSet = formset_factory(ReferenceForm)

        print(request.POST)
        character_creation_form = CharacterCreationForm(request.POST)
        relations_formset = RelationsFormSet(request.POST, prefix='relations-form')
        references_formset = ReferencesFormSet(request.POST, prefix='references-form')

        print(character_creation_form)
        print(relations_formset.cleaned_data)
        print(references_formset.cleaned_data)

