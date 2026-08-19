from django.db import models
from django.contrib.auth.models import User



class Movie(models.Model):

    # TMDb
    tmdb_id = models.IntegerField()

    # Movie or TV
    media_type = models.CharField(
        max_length=20,
        default="movie"
    )

    # Basic Info
    title = models.CharField(max_length=255)

    overview = models.TextField(
        blank=True,
        null=True
    )

    genre = models.CharField(
        max_length=255,
        blank=True
    )

    release_year = models.IntegerField(
        default=0
    )

    language = models.CharField(
        max_length=50,
        blank=True,
        default="English"
    )

    runtime = models.IntegerField(
        default=0
    )

    director = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    cast = models.TextField(
        blank=True,
        null=True
    )

    # Ratings
    rating = models.FloatField(
        default=0
    )

    popularity = models.FloatField(
        default=0
    )

    vote_count = models.IntegerField(
        default=0
    )

    # Images
    poster_url = models.URLField(
        blank=True
    )

    backdrop_url = models.URLField(
        blank=True
    )

    # Trailer (YouTube key from TMDb)
    trailer_key = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # Streaming URL
    video_url = models.URLField(
        blank=True,
        null=True
    )

    # Optional uploaded video
    video_file = models.FileField(
        upload_to="videos/",
        blank=True,
        null=True
    )

    # Home page category
    category = models.CharField(
        max_length=100,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["tmdb_id", "media_type"],
                name="unique_tmdb_media_type"
            )
        ]

    def __str__(self):
        return self.title

    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"

# =========================
# Continue Watching
# =========================

class ContinueWatching(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    progress = models.IntegerField(default=0)  # seconds watched
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "movie")

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"