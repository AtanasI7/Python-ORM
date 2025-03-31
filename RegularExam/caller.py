import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from main_app.choices import BookGenreChoices
from main_app.models import Publisher, Author, Book
from django.db.models import Q, Count, Avg, F


def get_publishers(search_string: str=None) -> str:
    if search_string is None:
        return "No search criteria."

    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string)
        |
        Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    if not publishers:
        return "No publishers found."

    result = []

    for p in publishers:
        result.append(f"Publisher: {p.name}, country: {'Unknown' if p.country == 'TBC' else p.country}, rating: {p.rating:.1f}")

    return '\n'.join(result)

def get_top_publisher() -> str:
    publisher = Publisher.objects.get_publishers_by_books_count().first()

    if publisher is None:
        return "No publishers found."

    return f"Top Publisher: {publisher.name} with {publisher.books_count} books."

def get_top_main_author() -> str:
    author = Author.objects.prefetch_related(
        'main_author_book'
    ).annotate(
        books_count=Count('main_author_book'),
        average_book_rating=Avg('main_author_book__rating')
    ).order_by('-books_count', 'name').first()

    if author is None or not author.books_count:
        return 'No results.'

    titles = [b.title for b in author.main_author_book.order_by('title')]

    return (f"Top Author: {author.name}, "
            f"own book titles: {', '.join(titles)}, "
            f"books average rating: {author.average_book_rating:.1f}")

def get_authors_by_books_count() -> str:
    authors = Author.objects.annotate(
        all_books_count=Count('main_author_book', distinct=True) + Count('co_author_books', distinct=True)
    ).order_by('-all_books_count', 'name')[:3]

    if not authors:
        return "No results."

    return '\n'.join(f"{a.name} authored {a.all_books_count} books." for a in authors)

def get_top_bestseller() -> str:
    book = Book.objects.prefetch_related(
        'main_author'
    ).prefetch_related(
        'co_authors'
    ).filter(
        is_bestseller=True
    ).order_by('-rating', 'title').first()

    if book is None:
        return 'No results.'

    co_authors = []

    for co in book.co_authors.order_by('name'):
        co_authors.append(co.name)

    return (f"Top bestseller: {book.title}, "
            f"rating: {book.rating:.1f}. "
            f"Main author: {book.main_author.name}. "
            f"Co-authors: {'N/A' if not co_authors else ', '.join(co_authors)}.")

def increase_price() -> str:
    books = Book.objects.filter(publication_date__year=2025, rating__gte=4.0)

    if not books:
        return "No changes in price."

    books.update(price=F('price') + F('price') * 0.20)

    return f"Prices increased for {books.count()} books."
























