import os
from datetime import timedelta, datetime

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.models import Author, Book, Artist, Song, Product, Review, DrivingLicense, Driver, Owner, Car, \
    Registration


# def show_all_authors_with_their_books():
#     authors = Author.objects.all().order_by('id')
#     authors_with_books = []
#
#     for author in authors:
#         books = Book.objects.filter(author=author)
#
#         if not books:
#             continue
#
#         titles = ', '.join(b.title for b in books)
#         authors_with_books.append(f'{author.name} has written - {titles}!')
#
#     return '\n'.join(authors_with_books)
#
# def delete_all_authors_without_books() -> None:
#     Author.objects.filter(book__isnull=True).delete()
#
#
# def add_song_to_artist(artist_name: str, song_title: str) -> None:
#     artist = Artist.objects.get(name=artist_name)
#     song = Song.objects.get(title=song_title)
#
#     artist.songs.add(song)
#
# def get_songs_by_artist(artist_name: str):
#     artist = Artist.objects.get(name=artist_name)
#
#     return artist.songs.all().order_by('-id')
#
# def remove_song_from_artist(artist_name: str, song_title: str) -> None:
#     artist = Artist.objects.get(name=artist_name)
#     song = Song.objects.get(title=song_title)
#
#     artist.songs.remove(song)
#
#
# def calculate_average_rating_for_product_by_name(product_name: str) -> float:
#     product = Product.objects.get(name=product_name)
#     reviews = product.reviews.all()
#
#     avg_rating = sum(r.rating for r in reviews) / len(reviews)
#
#     return avg_rating
#
# def get_reviews_with_high_ratings(threshold: int):
#     return Review.objects.filter(rating__gte=threshold)
#
# def get_products_with_no_reviews():
#     return Product.objects.filter(reviews__rating__isnull=True).order_by('-name')
#
# def delete_products_without_reviews() -> None:
#     Product.objects.filter(reviews__rating__isnull=True).delete()
#
#
# def calculate_licenses_expiration_dates():
#     licenses = DrivingLicense.objects.all().order_by('-license_number')
#     return '\n'.join(str(l) for l in licenses)
#
# def get_drivers_with_expired_licenses(due_date):
#     latest_issue_date = due_date - timedelta(days=365)
#     drivers_with_expired_licenses = Driver.objects.filter(license__issue_date__lt=latest_issue_date)
#
#     return drivers_with_expired_licenses
#
#
# def register_car_by_owner(owner: Owner):
#     car = Car.objects.filter(registration__isnull=True).first()
#     registration = Registration.objects.filter(car__isnull=True).first()
#
#     car.registration = registration
#     car.owner = owner
#
#     car.save()
#
#     registration.car = car
#     registration.registration_date = datetime.today()
#
#     registration.save()
#
#     return f"Successfully registered {car.model} to {owner.name} with registration number {registration.registration_number}."


def show_all_authors_with_their_books():
    authors = Author.objects.all().order_by('id')
    authors_with_books = []

    for author in authors:
        books = Book.objects.filter(author=author)

        if not books:
            continue

        titles = ', '.join(b.title for b in books)
        authors_with_books.append(f"{author.name} has written - {titles}!")

    return '\n'.join(authors_with_books)

# print(show_all_authors_with_their_books())


Author.objects.filter(id=8).delete()