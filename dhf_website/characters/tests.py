from django.test import TestCase, Client
from django.core.exceptions import FieldError, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from characters.models import Character
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

class CharacterCreationTests(TestCase):
    fixtures = ['users.json']

    def setUp(self):
        self.client = Client()

        self.character_data = {
            'name': 'Barbara Gordon',
            'f_status': 1,
            'series': 2,
            'relations': [
                {
                    'character_name': 'Dick Grayson',
                    'character_id': 1,
                    'summary': 'Barbara and Nightwing had a fling'
                }
            ]
        }

        self.valid_form_data = {
            'character_name': 'Test Name', 
            'character_series': 'Dummy series',
            'f_status': 'Yes',
        }

    def test_character_page_does_not_save_data_if_not_logged_in(self):

        response = self.client.post(f'/characters/{self.character_data["name"]}/', self.character_data)
        self.assertContains(response, 'Unauthorized', status_code=401)

    def test_character_page_does_save_data_if_logged_in(self):

        self.client.login(username='charcreationuser', password='dummyp@ss123')

        response = self.client.post(f'/characters/{self.character_data["name"]}/', self.character_data)

        self.assertContains(response, 'Success', status_code=200)

        raise Exception('Finish the test!')

    def test_character_creation_form_validation(self):
        test_form = CharacterCreationForm(self.valid_form_data)

        self.assertTrue(test_form.is_valid())
