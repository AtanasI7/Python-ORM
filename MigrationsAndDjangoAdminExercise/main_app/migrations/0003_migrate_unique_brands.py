# Generated by Django 5.0.4 on 2025-02-26 20:20

from django.db import migrations

def create_unique_brands(apps, schema_editor):
    Shoe = apps.get_model('main_app', 'Shoe')
    UniqueBrands = apps.get_model('main_app', 'UniqueBrands')

    unique_brands = Shoe.objects.values_list('brand', flat=True).distinct()
    unique_brands_to_add = [UniqueBrands(brand=brand_name) for brand_name in unique_brands]

    UniqueBrands.objects.bulk_create(unique_brands_to_add)

def deleted_unique_brands_data(apps, schema_editor):
    UniqueBrands = apps.get_model('main_app', 'UniqueBrands')
    UniqueBrands.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
    ]


