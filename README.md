<div align="center">

# 🎬 VibeStream

### Movie & TV Discovery Platform with Semantic Search and Personalization

<p>
  <strong>A Django-based streaming-style platform for discovering movies and TV shows, searching content, exploring recommendations, and managing a personal watchlist.</strong>
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
<img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL">
<img src="https://img.shields.io/badge/SQLite-Local%20DB-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
<img src="https://img.shields.io/badge/TMDb-API-01B4E4?style=flat-square" alt="TMDb">
<img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">

</div>

---

## 🌐 Live Demo

🚀 **VibeStream:**
https://vibestream-0k2c.onrender.com

💻 **Source Code:**
https://github.com/prachi912/VibeStream

VibeStream is deployed on **Render** with **PostgreSQL** used for the production database.

---

## 📸 Application Preview

### 🏠 Home & Content Discovery

![VibeStream Home Page](screenshots/home.png)

The home page provides a streaming-style interface for discovering trending, popular, top-rated, currently playing and upcoming content.

---

### 🔎 Search & Filtering

![VibeStream Search](screenshots/search.png)

The search system supports natural-language queries along with filters such as genre, year, language and rating.

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

One of the main technical components of VibeStream is its semantic-style search system.

Instead of relying only on exact movie titles, the application creates searchable text from movie metadata such as:

```text
Title
Genre
Overview
Language
Director
Cast
```

The search process works approximately as follows:

```text
Movie Metadata
      ↓
Text Representation
      ↓
TF-IDF Vectorization
      ↓
User Query Vector
      ↓
Cosine Similarity
      ↓
Keyword Matching
      ↓
Combined Relevance Score
      ↓
Ranked Results
```

The implementation uses **TfidfVectorizer** and **cosine_similarity** from Scikit-learn.

For example, users can search for:

```text
crime movies with psychological twists
```

or:

```text
dark mystery movies
```

The system compares the query against the movie metadata and ranks the most relevant results.

---

## 🎯 Content Similarity & Recommendations

VibeStream also uses the TF-IDF representation to identify movies with similar metadata.

```text
Selected Movie
      ↓
Movie TF-IDF Vector
      ↓
Cosine Similarity
      ↓
Compare with Catalog
      ↓
Remove Selected Movie
      ↓
Similar Content
```

This provides a lightweight **content-based recommendation approach** without requiring a large user-interaction dataset.

---

## 🎞️ TMDb Integration

VibeStream uses **The Movie Database (TMDb) API** as its external content source.

The application imports and stores information such as:

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

The imported information is stored in the application's database, allowing Django ORM queries to efficiently serve the application's discovery pages.

---

## 🔐 Authentication

Authentication is implemented using Django's authentication system and **Django Allauth**.

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

---

## ❤️ Watchlist & Continue Watching

### Watchlist

Authenticated users can save movies and TV content to their personal watchlist.

```text
User
  │
  └── WatchList
          │
          └── Movie
```

Each user's saved content is stored independently.

### Continue Watching

VibeStream stores viewing progress for authenticated users.

```text
User
  │
  └── ContinueWatching
          │
          ├── Movie
          ├── Progress
          └── Updated Time
```

This allows users to continue content from their previous viewing position.

---

## ▶️ Trailer Playback

VibeStream does **not** host a catalog of copyrighted movies.

Instead, available trailers are represented using trailer keys obtained through TMDb and displayed using YouTube-based playback.

```text
TMDb
 │
 └── Trailer Key
        ↓
   VibeStream
        ↓
   YouTube Trailer
```

The application therefore focuses on **content discovery and personalization** rather than building a full video-hosting platform.

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
| **Pandas**        | Data processing                   |
| **Scikit-learn**  | TF-IDF and cosine similarity      |
| **NumPy / SciPy** | Supporting numerical dependencies |

### 🗄️ Database

| Technology          | Purpose                    |
| ------------------- | -------------------------- |
| **SQLite**          | Local development database |
| **PostgreSQL**      | Production database        |
| **psycopg2**        | PostgreSQL database driver |
| **dj-database-url** | Database URL configuration |

### 🎨 Frontend

| Technology           | Purpose                       |
| -------------------- | ----------------------------- |
| **Django Templates** | Server-rendered UI            |
| **HTML5**            | Page structure                |
| **CSS3**             | Styling and responsive design |
| **JavaScript**       | Interactive functionality     |
| **YouTube Embeds**   | Trailer playback              |

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
        Django Templates                  TMDb API
        HTML / CSS / JS                      │
             │                               │
             └───────────────┬───────────────┘
                             │
                      Django Backend
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
        Views              Models          Search Engine
          │                  │                  │
          │                  │            Scikit-learn
          │                  │                  │
          └──────────────────┼──────────────────┘
                             │
                         Database
                      SQLite / PostgreSQL
                             │
                             ▼
                  User & Content Features
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

User-related functionality includes:

```text
WatchList
│
├── user
├── movie
└── added_at


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

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DEBUG=True

TMDB_API_KEY=your_tmdb_api_key

YOUTUBE_API_KEY=your_youtube_api_key

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

DATABASE_URL=your_database_url
```

Never commit `.env` or secret credentials to GitHub.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Import content

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

VibeStream is deployed using **Render**.

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

> ⚠️ Never commit API keys, OAuth secrets, database credentials or `.env` files to a public repository.

---

## 🚧 Engineering Challenges

### API Data Integration

Working with TMDb required handling external API responses, importing metadata and designing a database model capable of representing both movies and TV shows.

### Search & Ranking

A major challenge was moving beyond simple title matching.

The search implementation required:

1. Preparing searchable movie metadata.
2. Building a TF-IDF matrix.
3. Converting user queries into vectors.
4. Calculating cosine similarity.
5. Combining similarity with keyword matching.
6. Ranking the final results.

### Authentication

Supporting username/email login together with Google authentication required working with Django's authentication system, a custom authentication backend and Django Allauth.

### Local vs Production Database

The application uses SQLite during local development and PostgreSQL in production.

The database configuration is controlled through environment variables so the same Django application can work in both environments.

### Deployment

Deploying the project introduced practical challenges involving:

* Environment variables
* PostgreSQL configuration
* Static files
* URL routing
* Authentication configuration
* Production server configuration
* Debugging deployment issues

---

## 📚 What I Learned

Building VibeStream gave me practical experience with:

* Python and Django development
* Django ORM and relational databases
* Third-party REST API integration
* Data ingestion and processing
* Search and ranking techniques
* TF-IDF and cosine similarity
* Authentication and OAuth
* User-specific application features
* SQLite and PostgreSQL
* Environment configuration
* Static file handling
* Git and GitHub
* Production deployment
* Debugging development and deployment issues

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
* [x] Trending content
* [x] Category-based discovery
* [x] PostgreSQL production database
* [x] Render deployment
* [ ] Improved personalized recommendations
* [ ] More advanced recommendation models
* [ ] Improved search ranking
* [ ] Larger content catalog
* [ ] More detailed viewing analytics
* [ ] Performance optimization for larger datasets

---

## 🔮 Future Improvements

The next stage of VibeStream would focus on making recommendations more personalized.

```text
User Activity
      │
      ├── Viewing History
      │
      ├── Watchlist
      │
      └── Search History
              │
              ▼
      Recommendation Engine
              │
              ▼
     Personalized Content
```

Future versions could incorporate user behavior alongside content similarity to produce more personalized recommendations.

---

## 👩‍💻 About Me

### Prachi Chauhan

**MCA Graduate | Fresher | Aspiring Data Engineer**

Interested in building practical software and data-driven systems using:

**Python • SQL • Data Engineering • Cloud • AI/ML**

VibeStream was built as a hands-on project to strengthen my understanding of backend development, APIs, databases, machine learning techniques, authentication and production deployment.

<br>

<a href="https://github.com/prachi912">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github" alt="GitHub">
</a>

<a href="https://www.linkedin.com/in/prachi-chauhan-79a446226">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn">
</a>

---

<div align="center">

**VibeStream — built as a practical full-stack and data-focused learning project.**

</div>


