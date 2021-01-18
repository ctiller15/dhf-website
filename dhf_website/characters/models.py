from django.db import models
from django.db.models.functions import Length
from django.contrib.postgres.lookups import SearchLookup
from django.core.validators import MinLengthValidator

models.CharField.register_lookup(Length)
models.CharField.register_lookup(SearchLookup)

class F_Status(models.Model):
    name = models.CharField(max_length=20)

DEFAULT_F_STATUS_ID = 1

class Character(models.Model):
    # character_id PK
    name = models.CharField(max_length=200, blank=False, validators=[MinLengthValidator(1)])
    summary = models.CharField(max_length=500)
    # imagePath CharField-300
    hidden = models.BooleanField(default=False)
    f_status = models.ForeignKey(F_Status, on_delete=models.DO_NOTHING, default=DEFAULT_F_STATUS_ID)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gte=1),
                name="%(app_label)s_%(class)s_name_length",
            )
        ]
