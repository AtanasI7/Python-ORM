from email.policy import default

from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.choices import BookGenreChoices
from main_app.managers import PublisherManager


class NameCountryMixin(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3)
        ]
    )
    country = models.CharField(
        max_length=40,
        default='TBC'
    )

    class Meta:
        abstract = True

class RatingMixin(models.Model):
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        default=0.0
    )

    class Meta:
        abstract = True

class Publisher(NameCountryMixin, RatingMixin):
    established_date = models.DateField(
        default='1800-01-01'
    )
    objects = PublisherManager()

class Author(NameCountryMixin):
    birth_date = models.DateField(
        null=True,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

class Book(RatingMixin):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2)
        ]
    )
    publication_date = models.DateField()
    summary = models.TextField(
        null=True,
        blank=True
    )
    genre = models.CharField(
        max_length=11,
        choices=BookGenreChoices,
        default=BookGenreChoices.OTHER
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(9999.99)
        ],
        default=0.01
    )
    is_bestseller = models.BooleanField(
        default=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )
    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.CASCADE,
        related_name='publisher_book'
    )
    main_author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='main_author_book'
    )
    co_authors = models.ManyToManyField(
        Author,
        related_name='co_author_books'
    )






















