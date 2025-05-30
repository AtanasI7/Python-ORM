# Generated by Django 5.0.4 on 2025-02-27 17:23

from django.db import migrations


def add_age_groups_to_people(apps, schema_editor):
    Person = apps.get_model('main_app', 'Person')

    people = Person.objects.all()

    for person in people:
        if person.age <= 12:
            person.age_group = 'Child'
        elif person.age <= 17:
            person.age_group = 'Teen'
        else:
            person.age_group = 'Adult'

        person.save()

def set_age_group_default(apps, schema_editor):
    Person = apps.get_model('main_app', 'Person')
    default_age_group = Person.objects._meta.get_field('age_group').default

    people = Person.objects.all()


    for person in people:
        person.age_group = default_age_group
        person.save()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_person'),
    ]

    operations = [
        migrations.RunPython(add_age_groups_to_people, reverse_code=set_age_group_default)
    ]
