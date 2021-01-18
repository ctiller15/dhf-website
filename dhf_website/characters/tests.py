from django.test import TestCase
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
