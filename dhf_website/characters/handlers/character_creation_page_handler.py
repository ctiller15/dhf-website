from django.http import HttpResponse
from django.forms import formset_factory
from django.shortcuts import render, redirect
from characters.forms import CharacterCreationForm, ReferenceForm, RelationForm
from characters.models import Series, F_Status, Character, CharacterRelation, CharacterReference

def handle_character_creation(request):
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

