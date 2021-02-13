from django.test import TestCase, Client
from characters.models import Character, Series

class SeriesBrowserTest(TestCase):
    fixtures = ['f_status.json', 'series.json', 'characters.json', 'character_relations.json', 'character_references']

    def setUp(self):
        self.client = Client()

    def test_series_list_page_loads_all_series(self):
        response = self.client.get('/series/list/')
        response_str = str(response.content)

        series_set = Series.objects.all()

        self.assertEqual(response.status_code, 200)

        for series in series_set:
            self.assertIn(series.name, response_str)

    def test_series_page_loads_all_characters(self):
        response = self.client.get('/series/id=1/')
        response_str = str(response.content)

        character_list = Character.objects.filter(series__id=1)

        self.assertEqual(response.status_code, 200)

        for character in character_list:
            self.assertIn(character.name, response_str)
