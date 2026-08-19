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
            self.stdout.write(
                self.style.ERROR("TMDB_API_KEY not found")
            )
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

            self.stdout.write(
                f"Importing {category}..."
            )

            # Import first 5 pages
            for page in range(1, 6):

                url = (
                    f"{TMDB_BASE}/{endpoint}"
                    f"?api_key={api_key}&page={page}"
                )

                response = None

                # ---------------------------------
                # Retry up to 3 times
                # ---------------------------------

                for attempt in range(3):

                    try:

                        response = requests.get(
                            url,
                            timeout=60
                        )

                        response.raise_for_status()

                        break

                    except requests.RequestException as e:

                        if attempt == 2:

                            self.stdout.write(
                                self.style.WARNING(
                                    f"Skipping page {page} "
                                    f"of {category}: {e}"
                                )
                            )

                        else:

                            time.sleep(2)

                if response is None:
                    continue

                # ---------------------------------
                # Parse response
                # ---------------------------------

                try:
                    data = response.json()

                except ValueError:

                    self.stdout.write(
                        self.style.WARNING(
                            f"Invalid response on "
                            f"page {page} of {category}"
                        )
                    )

                    continue

                # ---------------------------------
                # Process each item
                # ---------------------------------

                for item in data.get("results", []):

                    tmdb_id = item.get("id")

                    if not tmdb_id:
                        continue

                    # ---------------------------------
                    # Title
                    # ---------------------------------

                    title = (
                        item.get("title")
                        or item.get("name")
                        or "Unknown"
                    )

                    # ---------------------------------
                    # Release year
                    # ---------------------------------

                    release = (
                        item.get("release_date")
                        or item.get("first_air_date")
                        or ""
                    )

                    try:

                        release_year = (
                            int(release[:4])
                            if release
                            else 0
                        )

                    except (ValueError, TypeError):

                        release_year = 0

                    # ---------------------------------
                    # Poster
                    # ---------------------------------

                    poster = (
                        POSTER_BASE + item["poster_path"]
                        if item.get("poster_path")
                        else ""
                    )

                    # ---------------------------------
                    # Backdrop
                    # ---------------------------------

                    backdrop = (
                        BACKDROP_BASE + item["backdrop_path"]
                        if item.get("backdrop_path")
                        else ""
                    )

                    # ---------------------------------
                    # Find existing movie
                    # ---------------------------------

                    existing_movie = Movie.objects.filter(
                        tmdb_id=tmdb_id,
                        media_type=media_type
                    ).first()

                    # ---------------------------------
                    # Permanent poster handling
                    #
                    # 1. TMDb has poster
                    #       → use it
                    #
                    # 2. TMDb has no poster
                    #       → keep existing poster
                    #
                    # 3. No existing poster
                    #       → empty string
                    # ---------------------------------

                    if poster:

                        poster_url = poster

                    elif (
                        existing_movie
                        and existing_movie.poster_url
                    ):

                        poster_url = existing_movie.poster_url

                    else:

                        poster_url = ""

                    # ---------------------------------
                    # Backdrop handling
                    # ---------------------------------

                    if backdrop:

                        backdrop_url = backdrop

                    elif (
                        existing_movie
                        and existing_movie.backdrop_url
                    ):

                        backdrop_url = (
                            existing_movie.backdrop_url
                        )

                    else:

                        backdrop_url = ""

                    # ---------------------------------
                    # Fetch additional details
                    # ---------------------------------

                    detail_url = (
                        f"{TMDB_BASE}/{media_type}/{tmdb_id}"
                        f"?api_key={api_key}"
                        f"&append_to_response=videos,credits"
                    )

                    detail = {}

                    try:

                        detail_response = requests.get(
                            detail_url,
                            timeout=60
                        )

                        if detail_response.status_code == 200:

                            detail = (
                                detail_response.json()
                            )

                    except requests.RequestException:

                        detail = {}

                    # ---------------------------------
                    # Genres
                    # ---------------------------------

                    genres = ", ".join(
                        g.get("name", "")
                        for g in detail.get(
                            "genres",
                            []
                        )
                        if g.get("name")
                    )

                    # ---------------------------------
                    # Trailer
                    # ---------------------------------

                    trailer_key = ""

                    videos = detail.get(
                        "videos",
                        {}
                    ).get(
                        "results",
                        []
                    )

                    # Prefer official trailer
                    for video in videos:

                        if (
                            video.get("site") == "YouTube"
                            and video.get("type") == "Trailer"
                            and video.get("official") is True
                        ):

                            trailer_key = (
                                video.get("key", "")
                            )

                            break

                    # Fallback to any YouTube trailer
                    if not trailer_key:

                        for video in videos:

                            if (
                                video.get("site") == "YouTube"
                                and video.get("type") == "Trailer"
                            ):

                                trailer_key = (
                                    video.get("key", "")
                                )

                                break

                    # ---------------------------------
                    # Director
                    # ---------------------------------

                    director = ""

                    for person in detail.get(
                        "credits",
                        {}
                    ).get(
                        "crew",
                        []
                    ):

                        if person.get("job") == "Director":

                            director = person.get(
                                "name",
                                ""
                            )

                            break

                    # ---------------------------------
                    # Cast
                    # ---------------------------------

                    cast = ", ".join(
                        actor.get("name", "")
                        for actor in detail.get(
                            "credits",
                            {}
                        ).get(
                            "cast",
                            []
                        )[:8]
                        if actor.get("name")
                    )

                    # ---------------------------------
                    # Runtime
                    # ---------------------------------

                    if media_type == "movie":

                        runtime = detail.get(
                            "runtime",
                            0
                        ) or 0

                    else:

                        episode_runtime = detail.get(
                            "episode_run_time",
                            []
                        )

                        runtime = (
                            episode_runtime[0]
                            if episode_runtime
                            else 0
                        )

                    # ---------------------------------
                    # Save / Update Movie
                    # ---------------------------------

                    Movie.objects.update_or_create(

                        tmdb_id=tmdb_id,

                        media_type=media_type,

                        defaults={

                            "title": title,

                            "overview": item.get(
                                "overview",
                                ""
                            ),

                            "genre": genres,

                            "release_year": release_year,

                            "language": item.get(
                                "original_language",
                                "en"
                            ),

                            "runtime": runtime,

                            "director": director,

                            "cast": cast,

                            "rating": item.get(
                                "vote_average",
                                0
                            ),

                            "popularity": item.get(
                                "popularity",
                                0
                            ),

                            "vote_count": item.get(
                                "vote_count",
                                0
                            ),

                            "poster_url": poster_url,

                            "backdrop_url": backdrop_url,

                            "trailer_key": trailer_key,

                            "category": category,

                            "media_type": media_type,
                        },
                    )

                    imported += 1

            # ---------------------------------
            # Small delay between endpoints
            # Helps avoid excessive API requests
            # ---------------------------------

            time.sleep(1)

        # ---------------------------------
        # Finished
        # ---------------------------------

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported/Updated {imported} "
                f"items successfully!"
            )
        )