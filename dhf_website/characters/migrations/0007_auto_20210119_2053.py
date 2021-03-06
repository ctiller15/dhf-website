# Generated by Django 3.1.5 on 2021-01-19 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('characters', '0006_auto_20210119_0422'),
    ]

    operations = [
        migrations.CreateModel(
            name='CharacterRelation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation_summary', models.CharField(max_length=2000)),
                ('character_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='character_1', to='characters.character')),
                ('character_2', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='character_2', to='characters.character')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='relations',
            field=models.ManyToManyField(related_name='_character_relations_+', through='characters.CharacterRelation', to='characters.Character'),
        ),
    ]
