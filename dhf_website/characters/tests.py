from django.test import TestCase, Client
from django.core.exceptions import FieldError, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from characters.models import Character, Series
from characters.forms import CharacterCreationForm

class CharacterModelTests(TestCase):
    fixtures = ['f_status.json']

    def test_characters_are_queryable(self):
        Character.objects.create(
            name="Betty Boop",
            hidden=False)

        self.assertTrue(len(Character.objects.all()) > 0)

    def test_characters_do_not_save_if_there_is_no_name(self):

        with transaction.atomic():
            self.assertRaises(IntegrityError, Character.objects.create, name="")
        self.assertEqual(len(Character.objects.all()), 0)

class CharacterPageTests(TestCase):

    fixtures = ['f_status.json', 'series.json', 'characters.json', 'character_relations.json', 'character_references']

    def setUp(self):
        self.client = Client()

    def test_character_page_loads_positive_data(self):
        response = self.client.get('/characters/Dick Grayson/')

        response_content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Dick Grayson', response_content)
        self.assertIn('Teen Titans', response_content)
        self.assertIn('Starfire', response_content)
        self.assertIn('Harley Quinn', response_content)
        self.assertIn('reference 1', response_content)

class CharacterBrowserTests(TestCase):
    fixtures = ['f_status.json', 'series.json', 'characters.json', 'character_relations.json', 'character_references']

    def setUp(self):
        self.client = Client()

    def test_character_list_page_loads_all_characters(self):
        response = self.client.get('/characters/list/')
        response_str = str(response.content)

        characters = Character.objects.all()

        self.assertEqual(response.status_code, 200)

        for character in characters:
            self.assertIn(character.name, response_str)

class CharacterCreationTests(TestCase):
    fixtures = ['f_status.json', 'users.json']

    def setUp(self):
        self.client = Client()

        self.character_data = {
            'character_name': 'Barbara Gordon',
            'f_status': 1,
            'character_series': 'Batman the animated series',
            'summary': 'Oracle. Also batgirl.',
            'relations-form-TOTAL_FORMS': 1,
            'relations-form-INITIAL_FORMS': 0,
            'relations-form-0-character_name': 'Dick Grayson',
            'relations-form-0-summary': 'They had a fling',
            'references-form-TOTAL_FORMS': 1,
            'references-form-INITIAL_FORMS': 0,
            'references-form-0-title': 'ref1'
        }

        self.second_character_data = {
            'character_name': 'Batman',
            'f_status': 1,
            'character_series': 'Batman the animated series',
            'character_series_id': 9,
            'summary': 'Oracle. Also batgirl.',
            'relations-form-TOTAL_FORMS': 1,
            'relations-form-INITIAL_FORMS': 0,
            'relations-form-0-character_name': 'Selina Kyle',
            'relations-form-0-summary': 'They had a fling',
            'references-form-TOTAL_FORMS': 1,
            'references-form-INITIAL_FORMS': 0,
            'references-form-0-title': 'ref1'
        }

        self.test_form_data = [
            (
                {
                'character_name': 'Test Name', 
                'character_series': 'Dummy series',
                'f_status': 1,
                }, True,
            ),
            (
                {
                    'character_name': '',
                    'character_series': 'New series',
                    'f_status': 1,
                }, False
            ),
            (
                {
                    'character_name': 'Bojack',
                    'character_series': '',
                    'f_status': 1,
                }, False
            ),
            (
                {
                    'character_name': 'Wally West',
                    'character_series': 'The flash',
                    'f_status': 'RaggleFraggle',
                }, False
            ),
        ]

    def test_character_page_does_not_save_data_if_not_logged_in(self):

        response = self.client.post(f'/characters/{self.character_data["character_name"]}/', self.character_data)
        self.assertContains(response, 'Unauthorized', status_code=401)

    def test_character_page_does_save_data_if_logged_in(self):

        seriesCountBefore = len(Series.objects.all())
        self.client.login(username='charcreationuser', password='dummyp@ss123')

        response = self.client.post(f'/characters/create/', self.character_data, follow=True)

        self.assertEqual(seriesCountBefore + 1, len(Series.objects.all()))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.templates[0].name, 'character_page.html')

        response_str = str(response.content)
        self.assertIn(self.character_data['character_name'], response_str)
        self.assertIn(self.character_data['character_series'], response_str)
        self.assertIn(self.character_data['summary'], response_str)
        self.assertIn(self.character_data['relations-form-0-character_name'], response_str)
        self.assertIn(self.character_data['relations-form-0-summary'], response_str)
        self.assertIn(self.character_data['references-form-0-title'], response_str)

    def test_character_page_does_not_save_duplicate_series_if_id_is_provided(self):
        seriesCountBefore = len(Series.objects.all())
        self.client.login(username='charcreationuser', password='dummyp@ss123')

        response = self.client.post(f'/characters/create/', self.character_data, follow=True)
        
        response2 = self.client.post(f'/characters/create/', self.second_character_data, follow=True)

        seriesCountAfter = len(Series.objects.all())

        self.assertEqual(seriesCountBefore, seriesCountAfter - 1)

    def test_character_creation_form_validation(self):
        for data, assertion in self.test_form_data:
            with self.subTest():

                test_form = CharacterCreationForm(data)

                self.assertEqual(test_form.is_valid(), assertion)
