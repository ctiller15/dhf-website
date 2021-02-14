from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.defaults import page_not_found
from search.forms import SearchForm
from characters.models import Character, Series
from itertools import chain

def search_character(request, term):
    exact_results = Character.objects.filter(name=term)
    fuzzy_results = Character.objects.filter(name__search=term)

    total_results = list(chain(exact_results, fuzzy_results))

    if len(exact_results) > 0:
        if len(exact_results) == 1:
            return redirect(f'/characters/{term}/')
        else:
            return render(request, 'character_multiple_found.html', context={ 'results': exact_results })
    elif len(fuzzy_results) > 0:
        return render(request, 'character_fuzzy_found.html', context={ 'results': fuzzy_results})
    else:
        return render(request, 'character_not_found.html', status=200)

def home(request):
    form = SearchForm()
    return render(request, "home.html", {'form': form })

def search(request):

    term = request.GET.get('search_term', None)
    return search_character(request, term)

def autocomplete_series(request):

    search_text = request.GET.get('search_text', None).lower()

    if request.method == 'GET':
        series_list = Series.objects.filter(name__icontains=search_text)

        updated_series_list = [{'name': series.name, 'id': series.id} for series in series_list]
        return JsonResponse({ 'series': updated_series_list})
