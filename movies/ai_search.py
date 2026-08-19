import re

from .models import Movie

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# SEARCH STATE
# =========================================================

_vectorizer = None
_movie_matrix = None
_movies = None


# =========================================================
# MOVIE DOCUMENT
# =========================================================

def movie_to_text(movie):
    

    return " ".join([
        f"Title: {movie.title or ''}",
        f"Genre: {movie.genre or ''}",
        f"Overview: {movie.overview or ''}",
        f"Language: {movie.language or ''}",
        f"Director: {movie.director or ''}",
        f"Cast: {movie.cast or ''}",
    ])


# =========================================================
# BUILD SEARCH INDEX
# =========================================================

def build_search_index():
    

    global _vectorizer
    global _movie_matrix
    global _movies

    _movies = list(
        Movie.objects.all()
    )

    if not _movies:
        _vectorizer = None
        _movie_matrix = None
        return

    documents = [
        movie_to_text(movie)
        for movie in _movies
    ]

    _vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=10000,
    )

    _movie_matrix = _vectorizer.fit_transform(
        documents
    )


# =========================================================
# KEYWORD MATCHING
# =========================================================

def keyword_score(query, movie):

    query_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower()
        )
    )

    if not query_words:
        return 0.0

    movie_text = movie_to_text(
        movie
    ).lower()

    matched = 0

    for word in query_words:

        if word in movie_text:
            matched += 1

    return matched / len(query_words)


# =========================================================
# SEARCH
# =========================================================

def semantic_search(query, top_n=30):

    global _vectorizer
    global _movie_matrix
    global _movies

    query = (query or "").strip()

    if not query:
        return []

    # Build the index when needed.
    if (
        _vectorizer is None
        or _movie_matrix is None
        or _movies is None
    ):
        build_search_index()

    if not _movies:
        return []

    # Convert query to TF-IDF vector.
    query_vector = _vectorizer.transform(
        [query]
    )

    # Calculate similarity against all movies.
    similarities = cosine_similarity(
        query_vector,
        _movie_matrix
    )[0]

    candidate_count = min(
        100,
        len(_movies)
    )

    candidate_indices = similarities.argsort()[
        -candidate_count:
    ][::-1]

    ranked_movies = []

    for index in candidate_indices:

        movie = _movies[index]

        similarity = float(
            similarities[index]
        )

        keyword = keyword_score(
            query,
            movie
        )

        # Combined score.
        final_score = (
            similarity * 0.85
            + keyword * 0.15
        )

        # Don't return completely unrelated movies.
        if final_score <= 0:
            continue

        ranked_movies.append(
            (
                final_score,
                movie
            )
        )

    # Highest relevance first.
    ranked_movies.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        movie
        for score, movie
        in ranked_movies[:top_n]
    ]


# =========================================================
# SIMILAR MOVIES
# =========================================================

def get_similar_movies(movie_id, top_n=10):

    global _vectorizer
    global _movie_matrix
    global _movies

    if (
        _vectorizer is None
        or _movie_matrix is None
        or _movies is None
    ):
        build_search_index()

    if not _movies:
        return []

    # Find target movie.
    target_index = None

    for index, movie in enumerate(_movies):

        if movie.id == movie_id:
            target_index = index
            break

    if target_index is None:
        return []

    target_vector = _movie_matrix[
        target_index
    ]

    similarities = cosine_similarity(
        target_vector,
        _movie_matrix
    )[0]

    result_count = min(
        top_n + 1,
        len(_movies)
    )

    candidate_indices = similarities.argsort()[
        -result_count:
    ][::-1]

    recommendations = []

    for index in candidate_indices:

        movie = _movies[index]

        # Don't recommend the same movie.
        if movie.id == movie_id:
            continue

        recommendations.append(
            movie
        )

        if len(recommendations) >= top_n:
            break

    return recommendations