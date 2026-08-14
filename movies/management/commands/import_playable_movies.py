import requests
from django.core.management.base import BaseCommand
from movies.models import Movie


class Command(BaseCommand):
    help = "Import playable streaming movies"

    def handle(self, *args, **kwargs):

        movies = [
            {
                "title": "Big Buck Bunny",
                "overview": "A giant rabbit takes revenge on a group of bullying rodents.",
                "genre": "Animation, Comedy",
                "release_year": 2008,
                "rating": 8.1,
                "poster_url": "https://download.blender.org/peach/bigbuckbunny_movies/poster/big_buck_bunny_poster_big.jpg",
                "backdrop_url": "https://download.blender.org/peach/bigbuckbunny_movies/poster/big_buck_bunny_poster_big.jpg",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                "category": "Streaming",
            },
            {
                "title": "Sintel",
                "overview": "A young woman searches for her lost dragon companion.",
                "genre": "Fantasy, Adventure",
                "release_year": 2010,
                "rating": 8.2,
                "poster_url": "https://download.blender.org/durian/poster/sintel_poster.jpg",
                "backdrop_url": "https://download.blender.org/durian/poster/sintel_poster.jpg",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
                "category": "Streaming",
            },
            {
                "title": "Tears of Steel",
                "overview": "Scientists and warriors unite in Amsterdam.",
                "genre": "Sci-Fi, Action",
                "release_year": 2012,
                "rating": 8.0,
                "poster_url": "https://mango.blender.org/wp-content/uploads/2013/05/01_thom_celia_bridge.jpg",
                "backdrop_url": "https://mango.blender.org/wp-content/uploads/2013/05/01_thom_celia_bridge.jpg",
                "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
                "category": "Streaming",
            },
        ]

        for i, movie in enumerate(movies, start=900000):

            Movie.objects.update_or_create(
                tmdb_id=i,
                defaults={
                    "title": movie["title"],
                    "overview": movie["overview"],
                    "genre": movie["genre"],
                    "release_year": movie["release_year"],
                    "rating": movie["rating"],
                    "popularity": 500,
                    "vote_count": 1000,
                    "poster_url": movie["poster_url"],
                    "backdrop_url": movie["backdrop_url"],
                    "video_url": movie["video_url"],
                    "category": movie["category"],
                },
            )

        self.stdout.write(self.style.SUCCESS("Streaming movies imported successfully."))