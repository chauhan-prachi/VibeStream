from sentence_transformers import SentenceTransformer, util
from .models import Movie

_model = None
_embeddings = None
_movies = None


# =========================
# Build AI Search Index
# =========================

def build_search_index():
    global _model, _embeddings, _movies

    _movies = list(Movie.objects.all())

    documents = []

    for movie in _movies:
        text = f"""
        Title: {movie.title or ""}
        Title: {movie.title or ""}

        Genre: {movie.genre or ""}
        Genre: {movie.genre or ""}
        Genre: {movie.genre or ""}
        Genre: {movie.genre or ""}

        Overview: {movie.overview or ""}
        Overview: {movie.overview or ""}
        Overview: {movie.overview or ""}
        Overview: {movie.overview or ""}
        Overview: {movie.overview or ""}

        Language: {movie.language or ""}
        """
        documents.append(text)

    _model = SentenceTransformer("all-MiniLM-L6-v2")
    _embeddings = _model.encode(documents, convert_to_tensor=True)


# =========================
# AI Semantic Search
# =========================

def semantic_search(query, top_n=20):
    global _model, _embeddings, _movies

    if _model is None:
        build_search_index()

    query_embedding = _model.encode(query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, _embeddings)[0]

    top_results = scores.topk(k=min(top_n, len(_movies)))

    results = []

    for idx in top_results.indices:
        movie = _movies[int(idx)]

        # Skip movies with missing posters
        if not movie.poster_url or movie.poster_url.strip() == "":
            continue

        results.append(movie)

        if len(results) >= top_n:
            break

    return results


# =========================
# AI Movie Recommendations
# =========================

def get_similar_movies(movie_id, top_n=10):
    global _model, _embeddings, _movies

    if _model is None:
        build_search_index()

    # Find the selected movie
    target_index = None

    for i, movie in enumerate(_movies):
        if movie.id == movie_id:
            target_index = i
            break

    if target_index is None:
        return []

    target_embedding = _embeddings[target_index]

    scores = util.cos_sim(target_embedding, _embeddings)[0]

    top_results = scores.topk(k=min(top_n + 1, len(_movies)))

    recommendations = []

    for idx in top_results.indices:
        idx = int(idx)
        movie = _movies[idx]

        # Skip the same movie
        if movie.id == movie_id:
            continue

        # Skip movies with missing posters
        if not movie.poster_url or movie.poster_url.strip() == "":
            continue

        recommendations.append(movie)

        if len(recommendations) >= top_n:
            break

    return recommendations