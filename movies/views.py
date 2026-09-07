from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Case, When
import json
import requests

from .models import Movie, WatchList, ContinueWatching


def home(request):
    print(
        "DATABASE ENGINE:",
        settings.DATABASES["default"]["ENGINE"]
    )

    print(
        "MOVIE COUNT:",
        Movie.objects.filter(
            media_type="movie"
        ).count()
    )

    print(
        "TV COUNT:",
        Movie.objects.filter(
            media_type="tv"
        ).count()
    )

    popular_movies = (
        Movie.objects
        .filter(media_type="movie")
        .order_by("-popularity")[:50]
    )

    top_rated_movies = (
        Movie.objects
        .filter(
            media_type="movie",
            category="Top Rated"
        )
        .order_by("-rating")[:50]
    )

    now_playing_movies = (
        Movie.objects
        .filter(
            media_type="movie",
            category="Now Playing"
        )
        .order_by("-popularity")[:50]
    )

    upcoming_movies = (
        Movie.objects
        .filter(
            media_type="movie",
            category="Upcoming"
        )
        .order_by("-release_year")[:50]
    )

    trending_tv = (
        Movie.objects
        .filter(media_type="tv")
        .order_by("-popularity")[:50]
    )

    top_series = (
        Movie.objects
        .filter(media_type="tv")
        .order_by("-rating")[:50]
    )

    featured_movies = list(
        Movie.objects
        .filter(media_type="movie")
        .exclude(poster_url="")
        .exclude(poster_url__isnull=True)
        .exclude(backdrop_url="")
        .exclude(backdrop_url__isnull=True)
        .order_by("-popularity")[:5]
    )

    featured_movie = (
        featured_movies[0]
        if featured_movies
        else None
    )

    watchlist_ids = set()

    if request.user.is_authenticated:
        watchlist_ids = set(
            WatchList.objects
            .filter(user=request.user)
            .values_list(
                "movie_id",
                flat=True
            )
        )

    context = {
        "featured_movie": featured_movie,
        "featured_movies": featured_movies,
        "popular_movies": popular_movies,
        "top_rated_movies": top_rated_movies,
        "now_playing_movies": now_playing_movies,
        "upcoming_movies": upcoming_movies,
        "trending_tv": trending_tv,
        "top_series": top_series,
        "watchlist_ids": watchlist_ids,
    }

    return render(
        request,
        "movies/home.html",
        context
    )


def search(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    year = request.GET.get("year", "").strip()
    language = request.GET.get("language", "").strip()
    rating = request.GET.get("rating", "").strip()
    sort = request.GET.get("sort", "").strip()

    movies = Movie.objects.all()

    if query:
        from .ai_search import semantic_search

        ai_results = semantic_search(
            query,
            top_n=100
        )

        ids = [movie.id for movie in ai_results]

        if ids:
            preserved_order = Case(
                *[
                    When(
                        id=movie_id,
                        then=position
                    )
                    for position, movie_id in enumerate(ids)
                ]
            )

            movies = (
                Movie.objects
                .filter(id__in=ids)
                .order_by(preserved_order)
            )
        else:
            movies = Movie.objects.none()

    if genre:
        movies = movies.filter(
            genre__icontains=genre
        )

    if year:
        try:
            movies = movies.filter(
                release_year=int(year)
            )
        except (ValueError, TypeError):
            pass

    if language:
        movies = movies.filter(
            language__iexact=language
        )

    if rating:
        try:
            movies = movies.filter(
                rating__gte=float(rating)
            )
        except (ValueError, TypeError):
            pass

    if sort == "rating":
        movies = movies.order_by(
            "-rating"
        )
    elif sort == "year":
        movies = movies.order_by(
            "-release_year"
        )
    elif sort == "popularity":
        movies = movies.order_by(
            "-popularity"
        )
    elif not query:
        movies = movies.order_by(
            "-popularity"
        )

    genres = (
        Movie.objects
        .exclude(genre__isnull=True)
        .exclude(genre="")
        .values_list(
            "genre",
            flat=True
        )
        .distinct()
    )

    years = (
        Movie.objects
        .exclude(release_year__isnull=True)
        .values_list(
            "release_year",
            flat=True
        )
        .distinct()
        .order_by("-release_year")
    )

    languages = (
        Movie.objects
        .exclude(language__isnull=True)
        .exclude(language="")
        .values_list(
            "language",
            flat=True
        )
        .distinct()
    )

    return render(
        request,
        "movies/search.html",
        {
            "movies": movies,
            "query": query,
            "genres": genres,
            "years": years,
            "languages": languages,
            "selected_genre": genre,
            "selected_year": year,
            "selected_language": language,
            "selected_rating": rating,
            "selected_sort": sort,
        },
    )


def movie_detail(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    from .ai_search import get_similar_movies

    recommendations = get_similar_movies(
        movie.id,
        top_n=10,
    )

    cast_members = []

    try:
        media_type = movie.media_type or "movie"

        url = (
            f"https://api.themoviedb.org/3/"
            f"{media_type}/{movie.tmdb_id}/credits"
        )

        response = requests.get(
            url,
            params={
                "api_key": settings.TMDB_API_KEY,
            },
            timeout=10,
        )

        if response.status_code == 200:
            data = response.json()

            cast_members = data.get(
                "cast",
                []
            )[:10]

    except Exception as e:
        print(
            "TMDb cast error:",
            e
        )

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "recommendations": recommendations,
            "cast_members": cast_members,
        },
    )


def watch_movie(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    if request.user.is_authenticated:
        ContinueWatching.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={
                "progress": 5
            },
        )

    youtube_key = None

    search_queries = [
        f"{movie.title} full movie official",
        f"{movie.title} full movie",
        f"{movie.title} official trailer",
        f"{movie.title} trailer",
    ]

    for query in search_queries:
        try:
            yt_response = requests.get(
                "https://www.googleapis.com/youtube/v3/search",
                params={
                    "part": "snippet",
                    "q": query,
                    "type": "video",
                    "maxResults": 5,
                    "key": settings.YOUTUBE_API_KEY,
                    "videoEmbeddable": "true",
                    "videoSyndicated": "true",
                },
                timeout=10,
            )

            if yt_response.status_code == 200:
                items = yt_response.json().get(
                    "items",
                    []
                )

                if items:
                    youtube_key = items[0]["id"]["videoId"]
                    break

        except requests.RequestException:
            pass

    if not youtube_key and movie.tmdb_id:
        try:
            tmdb_response = requests.get(
                f"https://api.themoviedb.org/3/"
                f"{movie.media_type}/{movie.tmdb_id}/videos",
                params={
                    "api_key": settings.TMDB_API_KEY
                },
                timeout=10,
            )

            if tmdb_response.status_code == 200:
                videos = tmdb_response.json().get(
                    "results",
                    []
                )

                official_trailer = None
                trailer = None

                for video in videos:
                    if video.get("site") != "YouTube":
                        continue

                    if (
                        video.get("type") == "Trailer"
                        and video.get("official")
                    ):
                        official_trailer = video.get("key")
                        break

                    elif (
                        video.get("type") == "Trailer"
                        and not trailer
                    ):
                        trailer = video.get("key")

                youtube_key = (
                    official_trailer
                    or trailer
                )

        except requests.RequestException:
            pass

    print(
        "MOVIE:",
        movie.title
    )

    print(
        "TMDB ID:",
        movie.tmdb_id
    )

    print(
        "FINAL YOUTUBE KEY:",
        youtube_key
    )

    if youtube_key:
        return redirect(
            f"https://www.youtube.com/watch?v={youtube_key}"
        )

    return redirect(
        "movie_detail",
        movie_id=movie.id
    )


@login_required
def remove_from_continue_watching(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    ContinueWatching.objects.filter(
        user=request.user,
        movie=movie,
    ).delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "profile"
        )
    )


@login_required
def add_to_watchlist(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    WatchList.objects.get_or_create(
        user=request.user,
        movie=movie,
    )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


@login_required
def remove_from_watchlist(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    WatchList.objects.filter(
        user=request.user,
        movie=movie,
    ).delete()

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "profile"
        )
    )


@login_required
def toggle_watchlist(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    item = WatchList.objects.filter(
        user=request.user,
        movie=movie,
    )

    if item.exists():
        item.delete()
    else:
        WatchList.objects.create(
            user=request.user,
            movie=movie,
        )

    return redirect(
        request.META.get(
            "HTTP_REFERER",
            "home"
        )
    )


def watchlist_page(request):
    watchlist = []

    if request.user.is_authenticated:
        watchlist = (
            WatchList.objects
            .filter(user=request.user)
            .select_related("movie")
            .order_by("-id")
        )

    return render(
        request,
        "movies/favorites.html",
        {
            "watchlist": watchlist,
        },
    )


@login_required
def continue_watching_page(request):
    continue_watching = (
        ContinueWatching.objects
        .filter(user=request.user)
        .select_related("movie")
        .order_by("-updated_at")
    )

    return render(
        request,
        "movies/continue_watching.html",
        {
            "continue_watching": continue_watching,
        },
    )


def categories_page(request):
    genre_movies = {}

    movies = Movie.objects.all()

    for movie in movies:
        if movie.genre:
            genres = [
                g.strip()
                for g in movie.genre.split(",")
            ]

            for genre in genres:
                if genre not in genre_movies:
                    genre_movies[genre] = []

                if len(genre_movies[genre]) < 12:
                    genre_movies[genre].append(movie)

    return render(
        request,
        "movies/categories.html",
        {
            "genre_movies": genre_movies,
        },
    )


def tv_page(request):
    tv_shows = (
        Movie.objects
        .filter(media_type="tv")
        .order_by("-popularity")
    )

    watchlist_ids = set()

    if request.user.is_authenticated:
        watchlist_ids = set(
            WatchList.objects
            .filter(user=request.user)
            .values_list(
                "movie_id",
                flat=True
            )
        )

    return render(
        request,
        "movies/tv.html",
        {
            "tv_shows": tv_shows,
            "watchlist_ids": watchlist_ids,
        },
    )


def favorites_page(request):
    watchlist = []

    if request.user.is_authenticated:
        watchlist = (
            WatchList.objects
            .filter(user=request.user)
            .select_related("movie")
            .order_by("-id")
        )

    return render(
        request,
        "movies/favorites.html",
        {
            "watchlist": watchlist,
        },
    )


@login_required
def profile_page(request):
    if request.method == "POST":
        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        if User.objects.filter(
            username=username
        ).exclude(
            id=request.user.id
        ).exists():

            watchlist = (
                WatchList.objects
                .filter(user=request.user)
                .select_related("movie")
            )

            continue_watching = (
                ContinueWatching.objects
                .filter(user=request.user)
                .select_related("movie")
                .order_by("-updated_at")[:10]
            )

            return render(
                request,
                "movies/profile.html",
                {
                    "watchlist": watchlist,
                    "continue_watching": continue_watching,
                    "watchlist_count": watchlist.count(),
                    "continue_count": continue_watching.count(),
                    "edit_mode": True,
                    "error": "Username already exists.",
                },
            )

        request.user.username = username
        request.user.email = email
        request.user.save()

        return redirect("profile")

    watchlist = (
        WatchList.objects
        .filter(user=request.user)
        .select_related("movie")
    )

    continue_watching = (
        ContinueWatching.objects
        .filter(user=request.user)
        .select_related("movie")
        .order_by("-updated_at")[:10]
    )

    context = {
        "watchlist": watchlist,
        "continue_watching": continue_watching,
        "watchlist_count": watchlist.count(),
        "continue_count": continue_watching.count(),
        "edit_mode": request.GET.get("edit") == "1",
    }

    return render(
        request,
        "movies/profile.html",
        context,
    )


@login_required
@require_POST
def save_progress(request, movie_id):
    movie = get_object_or_404(
        Movie,
        id=movie_id
    )

    data = json.loads(request.body)

    progress = int(
        data.get(
            "progress",
            0
        )
    )

    ContinueWatching.objects.update_or_create(
        user=request.user,
        movie=movie,
        defaults={
            "progress": progress
        },
    )

    return JsonResponse(
        {
            "status": "ok"
        }
    )


def browse(request, section):
    watchlist_ids = set()

    if request.user.is_authenticated:
        watchlist_ids = set(
            WatchList.objects
            .filter(user=request.user)
            .values_list(
                "movie_id",
                flat=True
            )
        )

    if section == "trending":
        movies = (
            Movie.objects
            .filter(media_type="movie")
            .order_by("-popularity")
        )

        title = "🔥 Trending Movies"

    elif section == "trending_tv":
        movies = (
            Movie.objects
            .filter(media_type="tv")
            .order_by("-popularity")
        )

        title = "📺 Trending TV Shows"

    elif section == "top_movies":
        movies = (
            Movie.objects
            .filter(media_type="movie")
            .order_by(
                "-rating",
                "-vote_count"
            )
        )

        title = "🏆 Top Movies This Week"

    elif section == "now_playing":
        movies = (
            Movie.objects
            .filter(
                media_type="movie",
                category="Now Playing"
            )
            .order_by("-popularity")
        )

        title = "🎭 Now Playing in Theaters"

    elif section == "top_series":
        movies = (
            Movie.objects
            .filter(media_type="tv")
            .order_by(
                "-rating",
                "-vote_count"
            )
        )

        title = "⭐ Top Series This Week"

    elif section == "dramas":
        movies = (
            Movie.objects
            .filter(
                genre__icontains="Drama"
            )
            .order_by("-popularity")
        )

        title = "🎭 Dramas"

    else:
        return redirect("home")

    return render(
        request,
        "movies/browse.html",
        {
            "movies": movies,
            "title": title,
            "watchlist_ids": watchlist_ids,
        },
    )