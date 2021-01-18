# Generated by Django 3.1.5 on 2021-01-14 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0004_auto_20210114_0100'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='character',
            constraint=models.CheckConstraint(check=models.Q(name__length__gte=1), name='characters_character_name_length'),
        ),
    ]
