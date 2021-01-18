from django.test import TestCase, Client
from search.forms import SearchForm

class HomePageTest(TestCase):
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

        raise Exception('Finish the test!')
