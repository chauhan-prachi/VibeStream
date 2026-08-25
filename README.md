<div align="center">

# 🎬 VibeStream

### Movie & TV Discovery Platform with Search, Content Similarity & Personalization

<p>
  <strong>
    A full-stack Django application for discovering movies and TV shows,
    searching content, finding similar titles, and managing personalized
    watchlists and viewing progress.
  </strong>
</p>

<br>

<a href="https://vibestream-0k2c.onrender.com">
  <img src="https://img.shields.io/badge/🚀%20Live%20Demo-VibeStream-8B5CF6?style=for-the-badge" alt="Live Demo">
</a>
&nbsp;
<a href="https://github.com/chauhan-prachi/VibeStream">
  <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repository">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
<img src="https://img.shields.io/badge/TMDb-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white" alt="TMDb">
<img src="https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">

</div>

---

## 📌 Overview

**VibeStream** is a full-stack movie and TV discovery platform built with **Python and Django**.

The application integrates the **TMDb API** to retrieve movie and TV metadata, stores content in a relational database, and provides search, filtering, content similarity, authentication, watchlists, viewing progress, and trailer playback.

A lightweight **content-search and ranking system** uses **TF-IDF, cosine similarity, and keyword matching** to help users discover relevant content beyond exact title matching.

The application is deployed on **Render with PostgreSQL** as the production database.

---

## 🌐 Live Demo

🚀 **[Open VibeStream](https://vibestream-0k2c.onrender.com)**

📂 **[View Source Code](https://github.com/chauhan-prachi/VibeStream)**

> The application is deployed on Render with PostgreSQL used as the production database.

---

## 📸 Application Preview

### 🏠 Home & Content Discovery

![VibeStream Home Page](screenshots/home.png)

Streaming-style interface for discovering popular, top-rated, trending, currently playing, and upcoming content.

### 🔎 Search & Filtering

![VibeStream Search](screenshots/search.png)

Search content using natural-language descriptions and refine results using genre, year, language, rating, and sorting options.

### 🎬 Movie Details

![VibeStream Movie Details](screenshots/movie-details.png)

Detailed content pages containing ratings, genres, overview, cast, director, release information, and available trailers.

### 📺 TV Shows

![VibeStream TV Shows](screenshots/tv-shows.png)

Dedicated discovery experience for TV content.

---

## ✨ Key Features

| Feature                      | Description                                                           |
| ---------------------------- | --------------------------------------------------------------------- |
| 🎬 **Movie Discovery**       | Browse popular, top-rated, upcoming, and currently playing movies     |
| 📺 **TV Discovery**          | Explore popular and trending TV shows                                 |
| 🔎 **Search & Filtering**    | Search and filter content by genre, year, language, rating, and more  |
| 🧠 **Semantic-Style Search** | Rank content using TF-IDF, cosine similarity, and keyword matching    |
| 🎯 **Content Similarity**    | Find similar movies using content-based similarity                    |
| 🔐 **Authentication**        | Registration, login, logout, profile management, and account deletion |
| 🔑 **Google OAuth**          | Sign in using Google through Django Allauth                           |
| ❤️ **Watchlist**             | Save movies and TV shows for later                                    |
| ▶️ **Continue Watching**     | Store and restore user viewing progress                               |
| 🎞️ **Trailer Playback**     | Play available trailers through YouTube                               |
| ☁️ **Production Deployment** | Django application deployed with Gunicorn, WhiteNoise, and PostgreSQL |

---

## 🧠 Search & Ranking System

One of the main technical components of VibeStream is its **content-based search and ranking system**.

Instead of relying only on exact title matching, the application represents movie information using fields such as:

* Title
* Genre
* Overview
* Language
* Director
* Cast

The search pipeline works approximately as follows:

```text
Movie Metadata
      ↓
Text Representation
      ↓
TF-IDF Vectorization
      ↓
User Query → TF-IDF Vector
      ↓
Cosine Similarity
      ↓
Keyword Matching
      ↓
Combined Relevance Score
      ↓
Ranked Results
```

The implementation uses `TfidfVectorizer` and `cosine_similarity` from **Scikit-learn**.

For example, users can search for:

```text
crime movies with psychological twists
```

or:

```text
dark mystery movies
```

The system compares the query against stored movie metadata and ranks relevant results.

> **Technical note:** This is a lightweight content-search approach based on TF-IDF and similarity scoring rather than a large neural embedding model.

---

## 🎯 Content Similarity & Recommendations

VibeStream uses the same content-based approach to identify movies with similar metadata.

```text
Selected Movie
      ↓
Movie Metadata
      ↓
TF-IDF Vector
      ↓
Cosine Similarity
      ↓
Compare with Catalog
      ↓
Rank Similar Content
```

This provides a practical recommendation approach without requiring a large user-interaction dataset.

---

## 🎞️ TMDb API Integration

VibeStream uses **The Movie Database (TMDb) API** as its external content source.

The application retrieves movie and TV metadata such as:

* Titles and TMDb IDs
* Genres and overviews
* Release information
* Languages and runtime
* Cast and director information
* Ratings and popularity
* Poster and backdrop URLs
* Trailer information
* Content categories

The retrieved data is transformed and stored in the application's database for efficient Django ORM queries.

A Django management command is used to import TMDb content:

```bash
python manage.py import_tmdb
```

### Data Flow

```text
TMDb API
   ↓
Django Management Command
   ↓
Data Transformation
   ↓
Django ORM
   ↓
PostgreSQL
   ↓
VibeStream Catalog
```

---

## 🔐 Authentication

Authentication is implemented using **Django's authentication system** and **Django Allauth**.

### Supported authentication features

* User registration
* Username/email login
* Password authentication
* Logout
* Google OAuth
* Profile management
* Account deletion
* User-specific watchlists
* User-specific viewing progress

A custom authentication backend allows users to authenticate using either their username or email address.

---

## ❤️ Watchlist

Authenticated users can save movies and TV shows to their personal watchlist.

Each watchlist is associated with the logged-in Django user, ensuring that saved content is user-specific.

```text
User
  │
  └── WatchList
        │
        └── Movie / TV Content
```

---

## ▶️ Continue Watching

VibeStream stores viewing progress for authenticated users.

```text
User
  │
  └── ContinueWatching
        ├── Movie
        ├── Progress
        └── Updated Time
```

This allows users to return to content and continue from their previous position.

---

## 🎥 Trailer Playback

VibeStream does **not host a catalog of copyrighted movies**.

Available trailers are displayed through YouTube-based playback using trailer information obtained through TMDb.

```text
TMDb
  │
  └── Trailer Information
          ↓
      VibeStream
          ↓
     YouTube Trailer
```

The project therefore focuses on **content discovery, search, personalization, and user experience** rather than video hosting.

---

## 🛠️ Technology Stack

| Category              | Technologies                                          |
| --------------------- | ----------------------------------------------------- |
| **Programming**       | Python 3.11                                           |
| **Backend**           | Django 5.2.16, Django ORM                             |
| **Authentication**    | Django Auth, Django Allauth, Google OAuth             |
| **Data & ML**         | Scikit-learn, TF-IDF, cosine similarity, NumPy, SciPy |
| **API Integration**   | TMDb API, Requests                                    |
| **Database**          | PostgreSQL, SQLite                                    |
| **Frontend**          | HTML5, CSS3, JavaScript, Django Templates             |
| **Production Server** | Gunicorn                                              |
| **Static Files**      | WhiteNoise                                            |
| **Deployment**        | Render                                                |
| **Version Control**   | Git, GitHub                                           |

---

## 🏗️ Application Architecture

```text
                         VibeStream
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ▼              ▼              ▼
          Django          TMDb API     Scikit-learn
          Backend             │         Search Engine
              │               │              │
              └───────────────┼──────────────┘
                              │
                              ▼
                         PostgreSQL
                              │
                              ▼
                    User-Specific Features
                   ┌──────────┴──────────┐
                   │                     │
               Watchlist          Viewing Progress
```

---

## 📁 Project Structure

```text
VibeStream/
│
├── accounts/
│   ├── migrations/
│   ├── backends.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── movies/
│   ├── management/
│   │   └── commands/
│   │       └── import_tmdb.py
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── ai_search.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── screenshots/
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Local Development

### 1. Clone the repository

```bash
git clone https://github.com/chauhan-prachi/VibeStream.git
cd VibeStream
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the environment

**Windows PowerShell:**

```powershell
venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True

TMDB_API_KEY=your_tmdb_api_key
YOUTUBE_API_KEY=your_youtube_api_key

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

DATABASE_URL=your_database_url
```

> Never commit `.env` files, API keys, OAuth secrets, or database credentials to GitHub.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Import TMDb content

```bash
python manage.py import_tmdb
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## ☁️ Deployment

VibeStream is deployed on **Render**.

```text
GitHub
   │
   ▼
Render
   │
   ├── Django
   ├── Gunicorn
   ├── WhiteNoise
   └── PostgreSQL
```

### Build Command

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### Start Command

```bash
gunicorn config.wsgi:application
```

The production database is configured using `DATABASE_URL`.

Secrets and environment-specific configuration are managed through the deployment environment rather than committed to the repository.

---

## 🔑 Environment Variables

| Variable               | Purpose                     |
| ---------------------- | --------------------------- |
| `SECRET_KEY`           | Django security key         |
| `DEBUG`                | Application debug mode      |
| `TMDB_API_KEY`         | TMDb API access             |
| `YOUTUBE_API_KEY`      | YouTube API access          |
| `GOOGLE_CLIENT_ID`     | Google OAuth client         |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret         |
| `DATABASE_URL`         | Database connection         |
| `ALLOWED_HOSTS`        | Allowed application domains |

---

## 🧩 Engineering Challenges

### API Data Integration

Handled external API responses, transformed relevant data, and persisted it in the application database using Django ORM.

### Search & Ranking

Implemented TF-IDF vectorization, cosine similarity, keyword matching, and result ranking to create a lightweight content-search system.

### Authentication

Implemented username/email authentication alongside Google OAuth using Django's authentication system and Django Allauth.

### Local vs Production Database

Configured the application to use SQLite for local development and PostgreSQL in production through environment-based database configuration.

### Production Deployment

Configured and deployed the Django application using:

* Render
* PostgreSQL
* Gunicorn
* WhiteNoise
* Environment variables
* Production Django settings

---

## 🗺️ Roadmap

* [x] Movie discovery
* [x] TV show discovery
* [x] TMDb API integration
* [x] Database-backed content catalog
* [x] User authentication
* [x] Google OAuth
* [x] Watchlist
* [x] Continue Watching
* [x] Search and filtering
* [x] Content similarity
* [x] Semantic-style search
* [x] PostgreSQL production database
* [x] Render deployment
* [ ] Personalized recommendations
* [ ] Improved ranking models
* [ ] In-app video/trailer player
* [ ] Viewing analytics
* [ ] Performance optimization for larger datasets

---

## 👩‍💻 About the Project

VibeStream was built as a hands-on project to apply concepts across:

**Software Development • Backend Engineering • Databases • APIs • Data Processing • Search & Information Retrieval • Machine Learning • Authentication • Cloud Deployment**

The project provided practical experience in designing, building, debugging, and deploying a complete web application.

---

## 👩‍💻 About Me

<div align="center">

### Prachi Chauhan

**MCA Graduate | Computer Science | Software • Data • Backend • AI/ML**

Interested in building practical software and data-driven systems using:

**Python • SQL • Django • PostgreSQL • Data Engineering • Cloud • AI/ML**

<br>

<a href="https://github.com/chauhan-prachi">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github" alt="GitHub">
</a>
&nbsp;
<a href="https://www.linkedin.com/in/prachi-chauhan-79a446226">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn">
</a>

</div>

---

<div align="center">

### 🎬 VibeStream

**A full-stack project combining web development, APIs, databases, search, and machine learning concepts.**

<br>

<a href="https://vibestream-0k2c.onrender.com">
  🚀 Live Demo
</a>

  •  

<a href="https://github.com/chauhan-prachi/VibeStream">
  💻 Source Code
</a>

</div>

