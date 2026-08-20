<div align="center">

# 🎬 VibeStream

### Movie & TV Discovery Platform with Semantic Search & Personalization

<p>
  <strong>Discover movies and TV shows, search naturally, explore similar content, and manage your personal watchlist in a modern streaming-style platform.</strong>
</p>

<br>

<a href="https://vibestream-0k2c.onrender.com">
  <img src="https://img.shields.io/badge/🚀%20Live%20Demo-VibeStream-8B5CF6?style=for-the-badge" alt="Live Demo">
</a>

<a href="https://github.com/prachi912/VibeStream">
  <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub Repository">
</a>

<br><br>

<img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Django-5.2-092E20?style=flat-square&logo=django&logoColor=white" alt="Django">
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
<img src="https://img.shields.io/badge/TMDb-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white" alt="TMDb">
<img src="https://img.shields.io/badge/Render-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">

<br><br>

> **VibeStream** is a full-stack Django application for movie and TV discovery. It combines TMDb data ingestion, database-backed content discovery, semantic-style search using TF-IDF and cosine similarity, authentication, watchlists, viewing progress and production deployment.

</div>

---

## 🌐 Live Demo

🚀 **Try VibeStream:**
https://vibestream-0k2c.onrender.com

📂 **Source Code:**
https://github.com/prachi912/VibeStream

> The application is deployed on Render with PostgreSQL used as the production database.

---

## 📸 Application Preview

### 🏠 Home & Content Discovery

![VibeStream Home Page](screenshots/home.png)

The home page provides a streaming-style interface for discovering trending, popular, top-rated, currently playing and upcoming content.

---

### 🔎 Search & Filtering

![VibeStream Search](screenshots/search.png)

The search system supports natural-language queries together with filters such as genre, year, language and rating.

---

### 🎬 Movie Details

![VibeStream Movie Details](screenshots/movie-details.png)

The movie details page displays information such as ratings, genres, overview, cast, director, release information and available trailer options.

---

### 📺 TV Shows

![VibeStream TV Shows](screenshots/tv-shows.png)

A dedicated section allows users to explore TV content separately from movies.

---

## ✨ Key Features

| Feature                      | Description                                                      |
| ---------------------------- | ---------------------------------------------------------------- |
| 🎬 **Movie Discovery**       | Browse popular, top-rated, upcoming and currently playing movies |
| 📺 **TV Discovery**          | Explore trending and popular TV shows                            |
| 🔎 **Semantic Search**       | Search content using natural-language descriptions               |
| 🧠 **Content Similarity**    | Find similar movies using TF-IDF and cosine similarity           |
| 🎯 **Search Filters**        | Filter content by genre, year, language and rating               |
| 📊 **Search Ranking**        | Rank results using similarity, keywords and content metadata     |
| 🔥 **Trending Content**      | Streaming-style featured content and discovery sections          |
| ❤️ **Watchlist**             | Save movies and shows for later                                  |
| ▶️ **Continue Watching**     | Store and restore viewing progress                               |
| 🔐 **Authentication**        | Registration, login, logout and account management               |
| 🔑 **Google Login**          | Google OAuth through Django Allauth                              |
| 🎞️ **Movie Details**        | Detailed information about movies and TV content                 |
| ▶️ **Trailer Playback**      | Play available trailers through YouTube                          |
| 🗂️ **Categories**           | Browse content through dedicated category pages                  |
| ☁️ **Production Deployment** | Django application deployed on Render with PostgreSQL            |

---

## 🧠 Semantic Search

A major technical component of VibeStream is its semantic-style search system.

Instead of relying only on exact title matching, the application represents movie information using fields such as:

```text
Title
Genre
Overview
Language
Director
Cast
```

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

The implementation uses `TfidfVectorizer` and `cosine_similarity` from Scikit-learn.

For example, users can search for:

```text
crime movies with psychological twists
```

or:

```text
dark mystery movies
```

The system uses the relationship between the query and stored movie metadata to rank relevant results.

> This is a lightweight content-search approach rather than a large-scale neural embedding system.

---

## 🎯 Content Similarity & Recommendations

VibeStream also uses TF-IDF and cosine similarity to identify content similar to the movie currently being viewed.

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
Remove Selected Movie
      ↓
Similar Content
```

This provides a practical content-based recommendation approach without requiring a large user-interaction dataset.

---

## 🎞️ TMDb Integration

VibeStream uses **The Movie Database (TMDb) API** as its external content source.

The application imports and stores metadata including:

* Movie and TV titles
* TMDb IDs
* Overview
* Genres
* Release year
* Language
* Runtime
* Director
* Cast
* Rating
* Popularity
* Vote count
* Poster URLs
* Backdrop URLs
* Trailer keys
* Content categories

The data is stored in the application's database so Django ORM queries can efficiently retrieve content for the different discovery pages.

The project includes a Django management command for importing TMDb content.

---

## 🔐 Authentication

Authentication is built around Django's authentication system and Django Allauth.

### Supported authentication

* User registration
* Username/email login
* Password authentication
* Logout
* Google OAuth
* Profile management
* Account deletion
* User-specific watchlists
* User-specific viewing progress

A custom authentication backend allows users to log in using either their username or email address.

Google authentication is handled through Django Allauth.

---

## ❤️ Watchlist

Authenticated users can save movies and TV shows to their personal watchlist.

The watchlist is associated with the logged-in Django user, meaning each account maintains its own saved content.

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

This allows the application to remember where a user stopped watching and provide a continue-watching experience.

---

## 🎥 Trailer Playback

VibeStream does **not** host a catalog of copyrighted movies.

Available trailers are displayed using YouTube-based playback with trailer information obtained through TMDb.

```text
TMDb
  │
  └── Trailer Key
        ↓
    VibeStream
        ↓
   YouTube Trailer
```

This keeps the project focused on **content discovery, search and personalization** rather than building a full video-hosting platform.

---

## 🛠️ Technology Stack

### 💻 Backend

| Technology              | Purpose                         |
| ----------------------- | ------------------------------- |
| **Python 3.11**         | Core programming language       |
| **Django 5.2.16**       | Web framework                   |
| **Django ORM**          | Database operations             |
| **Django Allauth**      | Authentication and Google OAuth |
| **Custom Auth Backend** | Username/email authentication   |
| **Gunicorn**            | Production WSGI server          |

### 🤖 Data & Machine Learning

| Technology        | Purpose                           |
| ----------------- | --------------------------------- |
| **TMDb API**      | Movie and TV metadata             |
| **Requests**      | API communication                 |
| **Scikit-learn**  | TF-IDF and cosine similarity      |
| **NumPy / SciPy** | Supporting numerical dependencies |

### 🗄️ Database

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| **SQLite**          | Local development          |
| **PostgreSQL**      | Production database        |
| **psycopg2**        | PostgreSQL database driver |
| **dj-database-url** | Database URL configuration |

### 🎨 Frontend

| Technology           | Purpose                         |
| -------------------- | ------------------------------- |
| **Django Templates** | Server-rendered pages           |
| **HTML5**            | Page structure                  |
| **CSS3**             | UI design and responsive layout |
| **JavaScript**       | Interactive functionality       |
| **YouTube Embeds**   | Trailer playback                |

### ☁️ Deployment

| Technology       | Purpose                            |
| ---------------- | ---------------------------------- |
| **Render**       | Production hosting                 |
| **Gunicorn**     | Application server                 |
| **WhiteNoise**   | Static file serving                |
| **Git / GitHub** | Version control and source hosting |

---

## 🏗️ Application Architecture

```text
                         VibeStream
                              │
              ┌───────────────┴───────────────┐
              │                               │
         Django Templates                 TMDb API
              │                               │
          HTML/CSS/JS                        │
              │                               │
              └───────────────┬───────────────┘
                              │
                       Django Backend
                              │
             ┌────────────────┼────────────────┐
             │                │                │
           Views            Models        Search Engine
             │                │                │
             │                │          Scikit-learn
             │                │                │
             └────────────────┼────────────────┘
                              │
                           Database
                       SQLite / PostgreSQL
                              │
                              ▼
                    User-Specific Features
                 Watchlist / Viewing Progress
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
│   │
│   ├── migrations/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   ├── templates/
│   │   └── movies/
│   │
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
│   ├── home.png
│   ├── search.png
│   ├── movie-details.png
│   └── tv-shows.png
│
├── templates/
├── static/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🗄️ Core Data Model

The main `Movie` model supports both movies and TV shows.

```text
Movie
│
├── tmdb_id
├── media_type
├── title
├── overview
├── genre
├── release_year
├── language
├── runtime
├── director
├── cast
├── rating
├── popularity
├── vote_count
├── poster_url
├── backdrop_url
├── trailer_key
├── video_url
├── video_file
└── category
```

User-specific models include:

```text
WatchList
│
├── user
├── movie
└── added_at
```

```text
ContinueWatching
│
├── user
├── movie
├── progress
└── updated_at
```

The `media_type` field allows the content model to represent:

```text
movie
tv
```

---

## ⚙️ Local Development

### 1. Clone the repository

```bash
git clone https://github.com/prachi912/VibeStream.git
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

> Never commit `.env`, API keys, OAuth secrets or database credentials to GitHub.

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

The production database is configured through `DATABASE_URL`.

Environment variables and secrets are configured through the Render dashboard rather than committed to the repository.

---

## 🔑 Environment Variables

| Variable               | Purpose                        |
| ---------------------- | ------------------------------ |
| `SECRET_KEY`           | Django security key            |
| `DEBUG`                | Application debug mode         |
| `TMDB_API_KEY`         | TMDb API access                |
| `YOUTUBE_API_KEY`      | YouTube API access             |
| `GOOGLE_CLIENT_ID`     | Google OAuth client            |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret            |
| `DATABASE_URL`         | Production database connection |
| `ALLOWED_HOSTS`        | Allowed application domains    |



---

## 🧪 Production Data

The application uses a database-backed catalog containing both movies and TV shows.

The catalog can be expanded through the TMDb import management command.

```text
TMDb API
   ↓
Import Command
   ↓
Django ORM
   ↓
PostgreSQL
   ↓
VibeStream Catalog
```

---

## 🧩 Engineering Challenges

### API Data Integration

Integrating TMDb required handling external API responses, transforming the returned data and storing the relevant fields in the application's database.

### Semantic Search

The search system required implementing:

1. Metadata text preparation
2. TF-IDF vectorization
3. Query vectorization
4. Cosine similarity
5. Keyword matching
6. Result ranking

This provided practical experience with search and information-retrieval concepts.

### Authentication

Supporting username/email authentication alongside Google OAuth required working with Django authentication, custom backend logic and Django Allauth.

### Local vs Production Database

SQLite is used for local development while PostgreSQL is used in production.

The database configuration is selected using environment variables so the same Django application can run in both environments.

### Deployment

Deploying the application introduced practical experience with:

* Environment variables
* PostgreSQL configuration
* Static files
* Gunicorn
* WhiteNoise
* Production settings
* URL routing
* Authentication configuration
* Debugging deployment issues

---

## 📚 What I Learned

Building VibeStream provided hands-on experience with:

* Python and Django development
* Django ORM
* Relational database design
* REST API integration
* Data ingestion
* Search and ranking
* TF-IDF and cosine similarity
* Authentication and OAuth
* User-specific application features
* SQLite and PostgreSQL
* Environment configuration
* Static file handling
* Git and GitHub
* Production deployment
* Debugging real-world application issues

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
* [x] Trending hero section
* [x] Category-based discovery
* [x] PostgreSQL production database
* [x] Render deployment
* [ ] Improved personalized recommendations
* [ ] More advanced recommendation models
* [ ] Expanded search capabilities
* [ ] Improved video delivery
* [ ] More detailed viewing analytics
* [ ] Performance optimization for larger datasets

---

## 🔮 Future Improvements

The next stage of VibeStream would focus on making recommendations more personalized.

```text
User Activity
      │
      ├── Viewing History
      ├── Watchlist
      └── Search History
              │
              ▼
      Recommendation Engine
              │
              ▼
      Personalized Content
```

Future improvements could include:

* User-behavior-based recommendations
* Improved ranking models
* Larger content catalogs
* Better search relevance
* More detailed analytics
* Recommendation evaluation
* Performance optimization
* Improved video delivery

---

## 👩‍💻 About Me

<div align="center">

### Prachi Chauhan

**MCA Graduate | Fresher | Aspiring Data Engineer**

Interested in building practical software and data-driven systems using:

**Python • SQL • Data Engineering • Cloud • AI/ML**

<br>

<a href="https://github.com/prachi912">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github" alt="GitHub">
</a>

<a href="https://www.linkedin.com/in/prachi-chauhan-79a446226">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn">
</a>

</div>

---

<div align="center">

### 🎬 VibeStream

**A hands-on project combining web development, APIs, databases, search and machine learning concepts.**

<br>

<a href="https://vibestream-0k2c.onrender.com">
  🚀 Live Demo
</a>
&nbsp;&nbsp;•&nbsp;&nbsp;
<a href="https://github.com/prachi912/VibeStream">
  💻 Source Code
</a>

<br><br>

*Built with Python, Django, SQL and machine learning techniques.*

</div>
