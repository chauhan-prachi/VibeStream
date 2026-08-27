import time

import requests

from django.core.management.base import BaseCommand
from django.conf import settings

from movies.models import Movie
from movies.services.data_cleaner import clean_movie_data


TMDB_BASE = "https://api.themoviedb.org/3"

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

            for page in range(1, 6):

                url = (
                    f"{TMDB_BASE}/{endpoint}"
                    f"?api_key={api_key}&page={page}"
                )

                response = None

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

                for item in data.get("results", []):

                    cleaned_data = clean_movie_data(item)

                    if not cleaned_data:
                        continue

                    tmdb_id = cleaned_data["tmdb_id"]

                    title = cleaned_data["title"]

                    release_year = cleaned_data["release_year"]

                    poster = (
                        POSTER_BASE + item["poster_path"]
                        if item.get("poster_path")
                        else ""
                    )

                    backdrop = (
                        BACKDROP_BASE + item["backdrop_path"]
                        if item.get("backdrop_path")
                        else ""
                    )

                    existing_movie = Movie.objects.filter(
                        tmdb_id=tmdb_id,
                        media_type=media_type
                    ).first()

                    if poster:

                        poster_url = poster

                    elif (
                        existing_movie
                        and existing_movie.poster_url
                    ):

                        poster_url = existing_movie.poster_url

                    else:

                        poster_url = ""

                    if backdrop:

                        backdrop_url = backdrop

                    elif (
                        existing_movie
                        and existing_movie.backdrop_url
                    ):

                        backdrop_url = existing_movie.backdrop_url

                    else:

                        backdrop_url = ""

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

                            detail = detail_response.json()

                    except requests.RequestException:

                        detail = {}

                    genres = ", ".join(
                        g.get("name", "")
                        for g in detail.get(
                            "genres",
                            []
                        )
                        if g.get("name")
                    )

                    trailer_key = ""

                    videos = detail.get(
                        "videos",
                        {}
                    ).get(
                        "results",
                        []
                    )

                    for video in videos:

                        if (
                            video.get("site") == "YouTube"
                            and video.get("type") == "Trailer"
                            and video.get("official") is True
                        ):

                            trailer_key = video.get(
                                "key",
                                ""
                            )

                            break

                    if not trailer_key:

                        for video in videos:

                            if (
                                video.get("site") == "YouTube"
                                and video.get("type") == "Trailer"
                            ):

                                trailer_key = video.get(
                                    "key",
                                    ""
                                )

                                break

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

                    Movie.objects.update_or_create(
                        tmdb_id=tmdb_id,
                        media_type=media_type,
                        defaults={
                            "title": title,
                            "overview": cleaned_data["overview"],
                            "genre": genres,
                            "release_year": release_year,
                            "language": cleaned_data["language"],
                            "runtime": runtime,
                            "director": director,
                            "cast": cast,
                            "rating": cleaned_data["rating"],
                            "popularity": cleaned_data["popularity"],
                            "vote_count": cleaned_data["vote_count"],
                            "poster_url": poster_url,
                            "backdrop_url": backdrop_url,
                            "trailer_key": trailer_key,
                            "category": category,
                            "media_type": media_type,
                        },
                    )

                    imported += 1

            time.sleep(1)

        self.stdout.write(
            self.style.SUCCESS(
                f"Imported/Updated {imported} "
                f"items successfully!"
            )
        )

        self.stdout.write(
            f"FINAL MOVIE COUNT: "
            f"{Movie.objects.filter(media_type='movie').count()}"
        )

        self.stdout.write(
            f"FINAL TV COUNT: "
            f"{Movie.objects.filter(media_type='tv').count()}"
        )