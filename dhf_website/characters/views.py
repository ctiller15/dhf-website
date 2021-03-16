from django.db.models import F, Q
from django.forms.models import model_to_dict
from django.shortcuts import render, redirect
from characters.models import Character, CharacterRelation, CharacterReference, F_Status, Series, CharacterReference
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from characters.forms import CharacterCreationForm, ReferenceForm, RelationForm
from django.forms import formset_factory
from django.conf import settings

def calculate_f_status_text(input_text):
    statuses = {
        'yes': 'Fucks',
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

        character_creation_form = CharacterCreationForm(request.POST, request.FILES)
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
                thumbnail=cleaned_character['thumbnail'],
                f_status=found_f_status,
                series=char_series,
            )

            cleaned_relations = [rel for rel in relations_formset.cleaned_data if rel]
            cleaned_references = [ref for ref in references_formset.cleaned_data if ref]

            for relation in cleaned_relations:
                if 'character_id' in relation and relation['character_id'] is not None:
                    char_relation = Character.objects.get(id=relation['character_id']) 
                elif 'character_name' in relation:
                    char_relation = Character.objects.create(
                        name=relation['character_name'],
                        f_status=found_f_status,
                        series=char_series,
                    )

                relation_obj = CharacterRelation.objects.create(character_1=new_character, character_2=char_relation, relation_summary=relation['summary'])

            for reference in cleaned_references:
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

def character_list(request):
    if request.method == 'GET':
        characters = Character.objects.all().order_by('name')

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
        character_id = request.POST.get('character_id')

        RelationsFormSet = formset_factory(RelationForm)
        ReferencesFormSet = formset_factory(ReferenceForm)

        character_creation_form = CharacterCreationForm(request.POST, request.FILES)
        #print(character_creation_form.is_multipart())

        if character_creation_form.is_valid():
            cleaned_character = character_creation_form.cleaned_data

            if cleaned_character['character_series_id']:
                char_series, created = Series.objects.get_or_create(id=cleaned_character['character_series_id'])
                if created:
                    char_series.name = cleaned_character['character_series']
                    char_series.save()
            else:
                char_series, created = Series.objects.get_or_create(name=cleaned_character['character_series'])

            found_f_status=F_Status.objects.get(id=cleaned_character['f_status'])

            character_to_update = Character.objects.get(id=character_id)

            character_to_update.name = cleaned_character['character_name']
            character_to_update.summary = cleaned_character['summary']
            character_to_update.series = char_series
            character_to_update.f_status = found_f_status
            character_to_update.thumbnail = cleaned_character['thumbnail']
            character_to_update.save()
            #character_to_update.update(name=cleaned_character['name'])

            relations_formset = RelationsFormSet(request.POST, prefix='relations-form')
            # find all of the new relations.
            relations = ( CharacterRelation.objects \
                .filter(character_1__id=character_id) \
                .values('relation_summary', character_name=F('character_2__name'), character_id=F('character_2__id')) ) \
                .union(CharacterRelation.objects \
               .filter(character_2__id=character_id) \
               .values('relation_summary', character_name=F('character_1__name'), character_id=F('character_1__id')))

            character_ids = [rel['character_id'] for rel in relations]

            character_names = [rel['character_name'] for rel in relations]

            # Update the old relations.
            for relation in relations_formset.cleaned_data:
                if relation['character_id'] in character_ids:
                    updated_relation = CharacterRelation.objects.filter(Q(character_2__id=relation['character_id'], character_1__id=character_id) | Q(character_2__id=character_id, character_1__id=relation['character_id'])).first()
                    updated_relation.summary = relation['summary']
                    updated_relation.save()
                    #print(relation)
                # get all ids that aren't the current character id.
                elif relation['character_name'] in character_names:
                    updated_relation = CharacterRelation.objects.filter(Q(character_2__name=relation['character_name'], character_1__id=character_id) | Q(character_2__id=character_id, character_1__name=relation['character_name'])).first()
                    updated_relation.summary = relation['summary']
                    updated_relation.save()
                else:
                    # Create the character.
                    found_f_status=F_Status.objects.get(name="yes")
                    old_character = Character.objects.get(id=character_id)
                    character = Character.objects.create(name=relation['character_name'], f_status=found_f_status)
                    new_relation = CharacterRelation.objects.create(character_1=old_character, character_2=character, relation_summary=relation['summary'])
                    # Create the relation.

            # For every relation NOT in the set, set it to hidden.

            # Save the new relations.
            references_formset = ReferencesFormSet(request.POST, prefix='references-form')

            print(references_formset.cleaned_data)

            references = CharacterReference.objects \
                .filter(character=character['id']) \
                .values('text')

            # if title not in references, add it to set of refrences.


            # and save the updated form data.
            # Save character

            # upsert relations
            # Find any combination of the relations
            # upsert references

            # redirect
            return redirect(f'/characters/char-id-{character_id}/')
