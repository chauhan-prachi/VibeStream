import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from movies.models import Movie

TMDB_BASE = "https://api.themoviedb.org/3"

# High quality image URLs
POSTER_BASE = "https://image.tmdb.org/t/p/w780"
BACKDROP_BASE = "https://image.tmdb.org/t/p/original"


class Command(BaseCommand):
    help = "Import movies and TV shows from TMDb"

    def handle(self, *args, **kwargs):

        api_key = settings.TMDB_API_KEY

        if not api_key:
            self.stdout.write(self.style.ERROR("TMDB_API_KEY not found"))
            return

        endpoints = [
    ("movie/popular", "Popular", "movie"),
    ("movie/top_rated", "Top Rated", "movie"),
    ("movie/now_playing", "Now Playing", "movie"),
    ("movie/upcoming", "Upcoming", "movie"),
    ("discover/movie", "Discover", "movie"),
    ("tv/popular", "TV Shows", "tv"),
    ("tv/top_rated", "TV Shows", "tv"),
    ("tv/on_the_air", "TV Shows", "tv"),
    ("tv/airing_today", "TV Shows", "tv"),
]

        imported = 0

        for endpoint, category, media_type in endpoints:

            self.stdout.write(f"Importing {category}...")

            # Import first 2 pages
            for page in range(1, 6):

                url = (
                    f"{TMDB_BASE}/{endpoint}"
                    f"?api_key={api_key}&page={page}"
                )

                response = None

                # Retry up to 3 times
                for attempt in range(3):
                    try:
                        response = requests.get(url, timeout=60)
                        response.raise_for_status()
                        break
                    except requests.RequestException as e:
                        if attempt == 2:
                            self.stdout.write(
                                self.style.WARNING(
                                    f"Skipping page {page} of {category}: {e}"
                                )
                            )
                        else:
                            time.sleep(2)

                if response is None:
                    continue

                data = response.json()

                for item in data.get("results", []):

                    title = item.get("title") or item.get("name")

                    release = (
                        item.get("release_date")
                        or item.get("first_air_date")
                        or ""
                    )

                    release_year = int(release[:4]) if release else 0

                    # High-quality poster
                    poster = (
                        POSTER_BASE + item["poster_path"]
                        if item.get("poster_path")
                        else ""
                    )

                    # High-quality backdrop
                    backdrop = (
                        BACKDROP_BASE + item["backdrop_path"]
                        if item.get("backdrop_path")
                        else ""
                    )

                    # Fetch additional details
                    detail_url = (
                        f"{TMDB_BASE}/{media_type}/{item['id']}"
                        f"?api_key={api_key}&append_to_response=videos,credits"
                    )

                    try:
                        detail = requests.get(detail_url, timeout=60).json()
                    except requests.RequestException:
                        detail = {}

                    # Genres
                    genres = ", ".join(
                        g["name"] for g in detail.get("genres", [])
                    )

                    # Trailer
                    trailer_key = ""
                    for video in detail.get("videos", {}).get("results", []):
                        if (
                            video.get("site") == "YouTube"
                            and video.get("type") == "Trailer"
                        ):
                            trailer_key = video.get("key")
                            break

                    # Director (movies only)
                    director = ""
                    for person in detail.get("credits", {}).get("crew", []):
                        if person.get("job") == "Director":
                            director = person.get("name", "")
                            break

                    # Cast
                    cast = ", ".join(
                        actor.get("name", "")
                        for actor in detail.get("credits", {}).get("cast", [])[:8]
                    )

                    Movie.objects.update_or_create(

                        tmdb_id=item["id"],
                        media_type=media_type,

                        defaults={

                            "title": title,

                            "overview": item.get("overview", ""),

                            "genre": genres,

                            "release_year": release_year,

                            "language": item.get(
                                "original_language",
                                "en",
                            ),

                            "runtime": detail.get(
                                "runtime",
                                detail.get("episode_run_time", [0])[0]
                                if detail.get("episode_run_time")
                                else 0,
                            ),

                            "director": director,

                            "cast": cast,

                            "rating": item.get("vote_average", 0),

                            "popularity": item.get("popularity", 0),

                            "vote_count": item.get("vote_count", 0),

                            "poster_url": poster,

                            "backdrop_url": backdrop,

                            "trailer_key": trailer_key,

                            "category": category,

                            "media_type": media_type,

                        },

                    )

                    imported += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported/Updated {imported} items successfully!"
            )
        )