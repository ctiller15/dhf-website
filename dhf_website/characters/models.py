from django.db import models
from django.db.models.functions import Length
from django.contrib.postgres.lookups import SearchLookup
from django.core.validators import MinLengthValidator

models.CharField.register_lookup(Length)
models.CharField.register_lookup(SearchLookup)

class F_Status(models.Model):
    name = models.CharField(max_length=20)

DEFAULT_F_STATUS_ID = 1

class Series(models.Model):
    name = models.CharField(max_length=200)

class Character(models.Model):
    # character_id PK
    name = models.CharField(max_length=200, blank=False, validators=[MinLengthValidator(1)])
    thumbnail = models.ImageField(upload_to='images/', null=True)
    summary = models.CharField(max_length=500)
    # imagePath CharField-300
    hidden = models.BooleanField(default=False)
    f_status = models.ForeignKey(F_Status, on_delete=models.DO_NOTHING, default=DEFAULT_F_STATUS_ID)
    series = models.ForeignKey(Series, on_delete=models.DO_NOTHING, null=True)
    relations = models.ManyToManyField("self", through='CharacterRelation')

    def first_char_group(self):
        if self.name:
            if not self.name[0].isalpha():
                return '#'
            else:
                return self.name[0]

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gte=1),
                name="%(app_label)s_%(class)s_name_length",
            )
        ]

class CharacterRelation(models.Model):
    character_1 = models.ForeignKey(Character, related_name="character_1", on_delete=models.CASCADE)
    character_2 = models.ForeignKey(Character, related_name="character_2", null=True, on_delete=models.CASCADE)
    relation_summary = models.CharField(max_length=2000)

class CharacterReference(models.Model):
    character = models.ForeignKey(Character, on_delete=models.DO_NOTHING)
    text = models.CharField(max_length=200)
