import os
import django


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()


from main_app.models import Director, Actor, Movie
from django.db.models import Q, Count, Avg, F


def get_directors(search_name=None, search_nationality=None):
    if search_name is None and search_nationality is None:
        return ""

    query_name = Q(full_name__icontains=search_name)
    query_nationality = Q(nationality__icontains=search_nationality)

    if search_name is not None and search_nationality is not None:
        query = Q(query_name & query_nationality)
    elif search_name is not None:
        query = query_name
    else:
        query = query_nationality

    directors = Director.objects.filter(query).order_by('full_name')

    if not directors:
        return ""

    result = []

    for d in directors:
        result.append(f"Director: {d.full_name}, nationality: {d.nationality}, experience: {d.years_of_experience}")

    return '\n'.join(result)

def get_top_director():
    director = Director.objects.get_directors_by_movies_count().first()

    if not director:
        return ""

    return f"Top Director: {director.full_name}, movies: {director.movies_count}."

def get_top_actor():
    actor = Actor.objects.prefetch_related('starring_movies').annotate(
        movies_count=Count('starring_movies'),
        avg_movie_rating=Avg('starring_movies__rating')
    ).order_by('-movies_count', 'full_name').first()

    if not actor or not actor.movies_count:
        return ""

    titles = ', '.join(m.title for m in actor.starring_movies.all())

    return (f"Top Actor: {actor.full_name}, "
            f"starring in movies: {titles}, "
            f"movies average rating: {actor.avg_movie_rating:.1f}")

def get_actors_by_movies_count():
    actors = Actor.objects.annotate(
        movies_count=Count('actor_movies')
    ).order_by('-movies_count', 'full_name')[:3]

    if not actors or not actors[0].movies_count:
        return ""

    result = []

    for a in actors:
        result.append(f'{a.full_name}, participated in {a.movies_count} movies')

    return '\n'.join(result)

def get_top_rated_awarded_movie():
    movie = Movie.objects.select_related(
        'starring_actor'
    ).prefetch_related(
        'actors'
    ).filter(is_awarded=True).order_by('-rating', 'title').first()

    if not movie:
        return ""

    starring_name = ''

    if not movie.starring_actor:
        starring_name = 'N/A'
    else:
        starring_name = movie.starring_actor.full_name

    actors = movie.actors.order_by('-full_name').values_list('full_name', flat=True)

    return (f"Top rated awarded movie: {movie.title}, "
            f"rating: {movie.rating:.1f}. "
            f"Starring actor: {starring_name}. "
            f"Cast: {', '.join(actors)}.")

def increase_rating():
    MAX_RATING = 10.0
    rating_increase = 0.1

    movies = Movie.objects.filter(is_classic=True, rating__lt=MAX_RATING)

    if not movies:
        return "No ratings increased."

    movies.update(rating=F("rating") + rating_increase)

    return f"Rating increased for {movies.count()} movies."




































