# Generated by Django 3.1.5 on 2021-01-14 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0002_auto_20210114_0028'),
    ]

    operations = [
        migrations.RenameField(
            model_name='f_status',
            old_name='Name',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='character',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
