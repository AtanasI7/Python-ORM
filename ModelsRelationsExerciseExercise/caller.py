import os
from datetime import datetime

import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Author, Book, Song, Artist, Review, Product, Driver, DrivingLicense, Owner, Registration, \
    Car


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

def delete_all_authors_without_books():
    Author.objects.filter(book__isnull=True).delete()


def add_song_to_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.add(song)

def get_songs_by_artist(artist_name: str):
    artist = Artist.objects.get(name=artist_name)
    songs = artist.songs.order_by('-id')

    return songs

def remove_song_from_artist(artist_name: str, song_title: str):
    artist = Artist.objects.get(name=artist_name)
    song = Song.objects.get(title=song_title)

    artist.songs.remove(song)

def calculate_average_rating_for_product_by_name(product_name: str):
    product = Product.objects.get(name=product_name)
    all_reviews = product.reviews.all()

    product_avg_ratings = sum(review.rating for review in all_reviews) / len(all_reviews)

    return product_avg_ratings

def get_reviews_with_high_ratings(threshold: int):
    reviews = Review.objects.filter(rating__gte=threshold)

    return reviews

def get_products_with_no_reviews():
    products = Product.objects.filter(reviews__rating__isnull=True).order_by('-name')

    return products

def delete_products_without_reviews():
    Product.objects.filter(reviews__rating__isnull=True).delete()


def register_car_by_owner(owner: Owner):
    registration = Registration.objects.filter(car__isnull=True).first()
    car = Car.objects.filter(registration__isnull=True).first()

    car.registration = registration
    car.registration.registration_date = datetime.today()
    car.owner = owner
    registration.car = car

    registration.save()
    car.save()

    return f"Successfully registered {car.model} to {car.owner.name} with registration number {registration.registration_number}."