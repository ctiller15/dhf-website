# Generated by Django 3.1.5 on 2021-02-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0008_characterreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='thumbnail',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]