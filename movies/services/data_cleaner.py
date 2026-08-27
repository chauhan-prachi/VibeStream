def clean_movie_data(item):
    if not isinstance(item, dict):
        return None

    tmdb_id = item.get("id")

    if not tmdb_id:
        return None

    try:
        tmdb_id = int(tmdb_id)
    except (ValueError, TypeError):
        return None

    title = (
        item.get("title")
        or item.get("name")
        or item.get("original_title")
        or item.get("original_name")
    )

    if not title:
        return None

    title = str(title).strip()

    overview = str(item.get("overview") or "").strip()

    language = str(
        item.get("original_language") or "en"
    ).strip().lower()

    try:
        rating = float(item.get("vote_average") or 0)
    except (ValueError, TypeError):
        rating = 0.0

    rating = max(0.0, min(rating, 10.0))

    try:
        popularity = float(item.get("popularity") or 0)
    except (ValueError, TypeError):
        popularity = 0.0

    try:
        vote_count = int(item.get("vote_count") or 0)
    except (ValueError, TypeError):
        vote_count = 0

    release = (
        item.get("release_date")
        or item.get("first_air_date")
        or ""
    )

    release_year = 0

    if release:
        try:
            release_year = int(str(release)[:4])
        except (ValueError, TypeError):
            release_year = 0

    return {
        "tmdb_id": tmdb_id,
        "title": title,
        "overview": overview,
        "language": language,
        "rating": rating,
        "popularity": popularity,
        "vote_count": vote_count,
        "release_year": release_year,
    }