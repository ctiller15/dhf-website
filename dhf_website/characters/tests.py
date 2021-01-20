from django.test import TestCase, Client
from django.core.exceptions import FieldError, ValidationError
from django.db import transaction
from django.db.utils import IntegrityError
from characters.models import Character

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

    fixtures = ['f_status.json', 'series.json', 'characters.json', 'character_relations.json']

    def setUp(self):
        self.client = Client()

    def test_character_page_loads_positive_data(self):
        response = self.client.get('/characters/Dick Grayson/')
        print(response)

        response_content = str(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertIn('Dick Grayson', response_content)
        self.assertIn('Teen Titans', response_content)
        self.assertIn('Starfire', response_content)
        self.assertIn('Harley Quinn', response_content)

        raise Exception('Finish the test!')
