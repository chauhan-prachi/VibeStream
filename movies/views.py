from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
import requests
from django.conf import settings
from .models import Movie, WatchList, ContinueWatching

# Home Page
# =========================
def home(request):
    print("DATABASE ENGINE:", settings.DATABASES["default"]["ENGINE"])
    print("MOVIE COUNT:", Movie.objects.count())
    popular_movies = (
        Movie.objects
        .order_by("-popularity")[:50]
    )

    top_rated_movies = (
        Movie.objects
        .filter(category="Top Rated")
        .order_by("-rating")[:50]
    )

    now_playing_movies = (
        Movie.objects
        .filter(category="Now Playing")
        .order_by("-popularity")[:50]
    )

    upcoming_movies = (
        Movie.objects
        .filter(category="Upcoming")
        .order_by("-release_year")[:50]
    )

    featured_movies = list(
        Movie.objects
        .filter(category="Popular")
        .order_by("-popularity")[:5]
    )

    featured_movie = featured_movies[0] if featured_movies else None
    watchlist_ids = set()

    if request.user.is_authenticated:
      watchlist_ids = set(
        WatchList.objects.filter(user=request.user)
        .values_list("movie_id", flat=True)
    )

    context = {
    "featured_movie": featured_movie,
    "featured_movies": featured_movies,
    "popular_movies": popular_movies,
    "top_rated_movies": top_rated_movies,
    "now_playing_movies": now_playing_movies,
    "upcoming_movies": upcoming_movies,
    "watchlist_ids": watchlist_ids,
}

    return render(request, "movies/home.html", context)

# =========================
# AI Semantic Search + Advanced Filters
# =========================

def search(request):
    query = request.GET.get("q", "").strip()
    genre = request.GET.get("genre", "").strip()
    year = request.GET.get("year", "").strip()
    language = request.GET.get("language", "").strip()
    rating = request.GET.get("rating", "").strip()
    sort = request.GET.get("sort", "").strip()

    # Start with all movies
    movies = Movie.objects.all()

    # AI semantic search
    if query:
        from .ai_search import semantic_search
        ai_results = semantic_search(query, top_n=50)
        ids = [m.id for m in ai_results]
        movies = Movie.objects.filter(id__in=ids)

    # Filters
    if genre:
        movies = movies.filter(genre__icontains=genre)

    if year:
        movies = movies.filter(release_year=year)

    if language:
        movies = movies.filter(language__iexact=language)

    if rating:
        movies = movies.filter(rating__gte=float(rating))

    # Sorting
    if sort == "rating":
        movies = movies.order_by("-rating")
    elif sort == "year":
        movies = movies.order_by("-release_year")
    else:
        movies = movies.order_by("-popularity")

    # Dropdown values
    genres = (
        Movie.objects.exclude(genre="")
        .values_list("genre", flat=True)
        .distinct()
    )

    years = (
        Movie.objects.exclude(release_year__isnull=True)
        .values_list("release_year", flat=True)
        .distinct()
        .order_by("-release_year")
    )

    languages = (
        Movie.objects.exclude(language="")
        .values_list("language", flat=True)
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

# =========================
# Movie Detail Page
# =========================

def movie_detail(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)
    from .ai_search import get_similar_movies
    # AI-powered recommendations
    recommendations = get_similar_movies(
        movie.id,
        top_n=10,
    )

    return render(
        request,
        "movies/movie_detail.html",
        {
            "movie": movie,
            "recommendations": recommendations,
        },
    )


# =========================
# Watch Page
# =========================

def watch_movie(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    # -------------------------
    # Add to Continue Watching
    # -------------------------
    if request.user.is_authenticated:
        ContinueWatching.objects.update_or_create(
            user=request.user,
            movie=movie,
            defaults={"progress": 5},
        )

    youtube_key = None

    # -------------------------
    # Search YouTube
    # -------------------------
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
                items = yt_response.json().get("items", [])
                if items:
                    youtube_key = items[0]["id"]["videoId"]
                    break

        except requests.RequestException:
            pass

    # -------------------------
    # Fallback to TMDb Trailer
    # -------------------------
    if not youtube_key and movie.tmdb_id:
        try:
            tmdb_response = requests.get(
                f"https://api.themoviedb.org/3/{movie.media_type}/{movie.tmdb_id}/videos",
                params={"api_key": settings.TMDB_API_KEY},
                timeout=10,
            )

            if tmdb_response.status_code == 200:
                videos = tmdb_response.json().get("results", [])

                official_trailer = None
                trailer = None

                for video in videos:

                    if video.get("site") != "YouTube":
                        continue

                    if video.get("type") == "Trailer" and video.get("official"):
                        official_trailer = video.get("key")
                        break

                    elif video.get("type") == "Trailer" and not trailer:
                        trailer = video.get("key")

                youtube_key = official_trailer or trailer

        except requests.RequestException:
            pass

    print("MOVIE:", movie.title)
    print("TMDB ID:", movie.tmdb_id)
    print("FINAL YOUTUBE KEY:", youtube_key)

    # -------------------------
    # Redirect directly to YouTube
    # -------------------------
    if youtube_key:
        return redirect(f"https://www.youtube.com/watch?v={youtube_key}")

    return redirect("movie_detail", movie_id=movie.id)


# =========================
# Remove from Continue Watching
# =========================

@login_required
def remove_from_continue_watching(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    ContinueWatching.objects.filter(
        user=request.user,
        movie=movie,
    ).delete()

    return redirect(
        request.META.get("HTTP_REFERER", "profile")
    )


# =========================
# Add to Watchlist
# =========================

@login_required
def add_to_watchlist(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    WatchList.objects.get_or_create(
        user=request.user,
        movie=movie,
    )

    return redirect(
        request.META.get("HTTP_REFERER", "home")
    )


# =========================
# Remove from Watchlist
# =========================

@login_required
def remove_from_watchlist(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    WatchList.objects.filter(
        user=request.user,
        movie=movie,
    ).delete()

    return redirect(
        request.META.get("HTTP_REFERER", "profile")
    )
# =========================
# Toggle Watchlist
# =========================

@login_required
def toggle_watchlist(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

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
        request.META.get("HTTP_REFERER", "home")
    )

# =========================
# Watchlist Page (See All)
# =========================

@login_required
def watchlist_page(request):

    watchlist = (
        WatchList.objects
        .filter(user=request.user)
        .select_related("movie")
    )

    return render(
        request,
        "movies/watchlist.html",
        {
            "watchlist": watchlist,
        },
    )


# =========================
# Continue Watching Page (See All)
# =========================

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

# ========================= 
# Categories Page 
# ========================= 
 
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
 
 
# ========================= 
# TV Page 
# ========================= 
 
def tv_page(request): 
 
    tv_shows = ( 
        Movie.objects 
        .filter(media_type="tv") 
        .order_by("-popularity") 
    ) 
 
    return render( 
        request, 
        "movies/tv.html", 
        { 
            "tv_shows": tv_shows, 
        }, 
    ) 
 
 
# =========================
# Favorites / My List Page
# =========================

@login_required
def favorites_page(request):

    watchlist = WatchList.objects.filter(
        user=request.user
    ).select_related("movie").order_by("-id")

    return render(
        request,
        "movies/favorites.html",
        {
            "watchlist": watchlist,
        },
    )
 
 
# ========================= 
# Profile Page 
# ========================= 
 
from django.contrib.auth.models import User 
 
@login_required 
def profile_page(request): 
 
    # ------------------------- 
    # Handle Edit Profile 
    # ------------------------- 
    if request.method == "POST": 
 
        username = request.POST.get("username", "").strip() 
        email = request.POST.get("email", "").strip() 
 
        # Prevent duplicate usernames 
        if User.objects.filter(username=username).exclude(id=request.user.id).exists(): 
 
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
 
    # ------------------------- 
    # Normal Profile View 
    # ------------------------- 
 
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
# ========================= 
# Save Video Progress 
# ========================= 
 
@login_required 
@require_POST 
def save_progress(request, movie_id): 
 
    movie = get_object_or_404(Movie, id=movie_id) 
 
    data = json.loads(request.body) 
 
    progress = int(data.get("progress", 0)) 
 
    ContinueWatching.objects.update_or_create( 
        user=request.user, 
        movie=movie, 
        defaults={"progress": progress}, 
    ) 
 
    return JsonResponse({"status": "ok"})   
