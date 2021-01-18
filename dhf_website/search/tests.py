from django.test import TestCase, Client
from search.forms import SearchForm
from characters.models import Character

class HomePageTest(TestCase):
    fixtures = ['f_status.json']

    def setUp(self):
        self.client = Client()

    def test_home_page_loads(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
    
    def test_home_page_form(self):
        form = SearchForm()
        self.assertFalse(form.is_valid())

    def test_home_page_form_requires_data(self):
        data = {
            "search_term": "dummy_search_term"
        }

        form = SearchForm(data)
        self.assertTrue(form.is_valid())

    def test_searching_nonexistent_character_renders_404_view(self):

        response = self.client.get('/search?search_term=popeye')

        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.templates[0].name, 'character_not_found.html')

    def test_searching_multiple_characters_renders_multiple_found_view(self):

        Character.objects.create(name="popeye")
        Character.objects.create(name="popeye")

        response = self.client.get('/search?search_term=popeye')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'character_multiple_found.html')

    def test_searching_characters_without_exact_matches_renders_fuzzy_find_view(self):

        Character.objects.create(name="popeye the sailor man")

        response = self.client.get('/search?search_term=sailor')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'character_fuzzy_found.html')

    def test_searching_exact_matches_renders_character_page(self):

        Character.objects.create(name="Bojack Horseman")

        response = self.client.get('/search?search_term=Bojack Horseman')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'character_page.html')
