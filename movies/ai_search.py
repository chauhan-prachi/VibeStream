import re

from .models import Movie

# AI SEARCH STATE
print("MOVIE COUNT:", Movie.objects.count())
_model = None
_embeddings = None
_movies = None

# LOAD MODEL

def get_model():
    

    global _model

    if _model is None:
        # Import 

        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model

# MOVIE DOCUMENT

def movie_to_text(movie):
    """
    Convert movie information into one meaningful
    text document for semantic search.
    """

    return " ".join([
        f"Title: {movie.title or ''}",
        f"Genre: {movie.genre or ''}",
        f"Overview: {movie.overview or ''}",
        f"Language: {movie.language or ''}",
        f"Director: {movie.director or ''}",
        f"Cast: {movie.cast or ''}",
    ])


# BUILD SEARCH INDEX

def build_search_index():
    """
    Load movies from PostgreSQL/SQLite and create
    their embeddings once per worker.
    """

    global _embeddings, _movies

    model = get_model()

    _movies = list(
        Movie.objects.all()
    )

    if not _movies:
        _embeddings = None
        return

    documents = [
        movie_to_text(movie)
        for movie in _movies
    ]

    _embeddings = model.encode(
        documents,
        convert_to_tensor=True,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

# KEYWORD MATCHING

def keyword_score(query, movie):
    

    query_words = set(
        re.findall(
            r"\b[a-zA-Z0-9]+\b",
            query.lower()
        )
    )

    if not query_words:
        return 0.0

    movie_text = " ".join([
        movie.title or "",
        movie.genre or "",
        movie.overview or "",
        movie.language or "",
        movie.director or "",
        movie.cast or "",
    ]).lower()

    matched = 0

    for word in query_words:
        if word in movie_text:
            matched += 1

    return matched / len(query_words)


# AI SEMANTIC SEARCH

def semantic_search(query, top_n=30):
    

    global _embeddings, _movies

    query = (query or "").strip()

    if not query:
        return []

    # Build index only when required.
    if _embeddings is None or _movies is None:
        build_search_index()

    if not _movies or _embeddings is None:
        return []

    model = get_model()

    #  user's query.
    query_embedding = model.encode(
        query,
        convert_to_tensor=True,
        normalize_embeddings=True,
    )

    from sentence_transformers import util

    semantic_scores = util.cos_sim(
        query_embedding,
        _embeddings
    )[0]

   
    candidate_count = min(
        100,
        len(_movies)
    )

    top_results = semantic_scores.topk(
        k=candidate_count
    )

    ranked_movies = []

    for idx, semantic_score in zip(
        top_results.indices,
        top_results.values
    ):
        idx = int(idx)

        movie = _movies[idx]

        semantic_score = float(
            semantic_score
        )

        # Keyword relevance.
        keyword = keyword_score(
            query,
            movie
        )

        
        final_score = (
            semantic_score * 0.85
            + keyword * 0.15
        )

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

   
    results = [
        movie
        for score, movie in ranked_movies[:top_n]
    ]

    return results


# SIMILAR MOVIES

def get_similar_movies(movie_id, top_n=10):
   
    global _embeddings, _movies

    if _embeddings is None or _movies is None:
        build_search_index()

    if not _movies or _embeddings is None:
        return []

    # Find target movie.
    target_index = None

    for index, movie in enumerate(_movies):

        if movie.id == movie_id:
            target_index = index
            break

    if target_index is None:
        return []

    from sentence_transformers import util

    target_embedding = _embeddings[
        target_index
    ]

    scores = util.cos_sim(
        target_embedding,
        _embeddings
    )[0]

    # +1 because the movie itself will be removed.
    result_count = min(
        top_n + 1,
        len(_movies)
    )

    top_results = scores.topk(
        k=result_count
    )

    recommendations = []

    for idx in top_results.indices:

        idx = int(idx)

        movie = _movies[idx]

        # not recommend the same movie.
        if movie.id == movie_id:
            continue

        recommendations.append(movie)

        if len(recommendations) >= top_n:
            break

    return recommendations
