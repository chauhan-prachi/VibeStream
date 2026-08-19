<div align="center">

# 🎬 VibeStream

### Streaming Content Discovery, Analytics & Recommendation Platform

<p>
  <strong>
    Discover movies and TV shows, search content, explore trending titles,
    manage your watchlist, and continue watching through a modern
    streaming-style platform.
  </strong>
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
<img src="https://img.shields.io/badge/TMDb-API-01B4E4?style=flat-square&logo=themoviedatabase&logoColor=white" alt="TMDb">
<img src="https://img.shields.io/badge/Scikit--learn-ML-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
<img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">

<br><br>

> **VibeStream** is a full-stack Django web application built to explore and organize movie and TV content through a modern streaming-style interface. It combines external movie data, database-backed content discovery, search and filtering, user authentication, watchlists, viewing progress, and recommendation-oriented features into a single platform.

</div>

---

## 🌐 Live Demo

🚀 **Try VibeStream:**

**https://vibestream-0k2c.onrender.com**

📦 **Source Code:**

**https://github.com/prachi912/VibeStream**

> VibeStream is deployed on Render with PostgreSQL used as the production database.

---

# 📸 Application Preview

> Screenshots can be added to this section later. GitHub repository screenshots are recommended because they allow recruiters to quickly understand the project visually.

### 🏠 Home & Content Discovery

*Add a screenshot of the VibeStream home page here.*

The home page provides a streaming-style interface with featured content, trending movies, top-rated titles, now-playing content, upcoming releases, and TV sections.

---

### 🔎 Search & Filtering

*Add a screenshot of the search page here.*

Users can search the content catalog and narrow results using available filters such as genre, year, language, rating, and sorting options.

---

### 🎬 Movie Details

*Add a screenshot of a movie detail page here.*

The movie detail page presents information such as title, overview, rating, release year, genres, cast, director, poster, backdrop, and trailer information.

---

### 📺 TV Shows

*Add a screenshot of the TV Shows page here.*

The TV section provides a dedicated discovery experience for television content.

---

### ❤️ Watchlist

*Add a screenshot of the Watchlist page here.*

Authenticated users can save movies and TV shows to their personal watchlist.

---

### 👤 Profile & Authentication

*Add a screenshot of the profile/authentication interface here.*

Users can create accounts, log in, manage their profile, and use Google authentication.

---

# ✨ Features

| Feature                         | Description                                                                         |
| ------------------------------- | ----------------------------------------------------------------------------------- |
| 🎬 **Movie Discovery**          | Browse popular, top-rated, upcoming, and currently playing movies                   |
| 📺 **TV Show Discovery**        | Explore TV content through a dedicated discovery section                            |
| 🔎 **Search & Filtering**       | Search and filter content using multiple criteria                                   |
| 🎯 **Content Recommendations**  | Recommendation-oriented functionality based on movie metadata and user interactions |
| 🔥 **Trending Hero Section**    | Rotating featured movies with cinematic backdrop images                             |
| ❤️ **Watchlist / My List**      | Save movies and shows for later                                                     |
| ▶️ **Continue Watching**        | Track viewing progress and resume content                                           |
| 🔐 **User Authentication**      | User registration, login, logout, and account management                            |
| 🔑 **Google OAuth**             | Google authentication through Django Allauth                                        |
| 🎞️ **Movie Details**           | Display ratings, genres, cast, directors, descriptions, and metadata                |
| 🎥 **Trailer Support**          | Display available trailer content                                                   |
| 🗂️ **Categories**              | Organized content discovery through multiple categories                             |
| 📱 **Responsive UI**            | Streaming-inspired interface for different screen sizes                             |
| ☁️ **Cloud Deployment**         | Production deployment using Render and PostgreSQL                                   |
| 🗄️ **Database-backed Catalog** | Movie and TV metadata stored and queried through Django ORM                         |

---

# 🎯 How VibeStream Works

```text
                         ┌─────────────────────┐
                         │      VibeStream     │
                         │   Web Application   │
                         └──────────┬──────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
                ▼                   ▼                   ▼
          🔎 Search            🎬 Discovery          👤 Account
                │                   │                   │
                ▼                   ▼                   ▼
        Search & Filters      Movie / TV Data     Authentication
                │             & Categories        & Watchlist
                │                   │                   │
                └───────────────────┼───────────────────┘
                                    ▼
                          ┌──────────────────┐
                          │ Django Backend   │
                          └────────┬─────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
                  ▼                ▼                ▼
              TMDb API       PostgreSQL        ML / Search
                  │                │                │
                  └────────────────┼────────────────┘
                                   ▼
                         🎬 Content Results
```

---

# 🧠 Search & Recommendation

VibeStream is designed to move beyond a basic movie-list application by incorporating search and recommendation-oriented functionality.

Users can explore content through:

* Movie titles
* Genres
* Ratings
* Release years
* Languages
* Popularity
* Categories
* Natural-language search where supported

The recommendation functionality uses available movie metadata and machine-learning techniques to identify content with similar characteristics.

The goal is to make content discovery more relevant than simply displaying a static catalog.

---

# 🎞️ TMDb Integration

VibeStream uses **The Movie Database (TMDb) API** as the primary external source for movie and TV metadata.

The application works with information including:

* Movie and TV titles
* Posters
* Backdrops
* Genres
* Ratings
* Popularity
* Vote counts
* Release information
* Runtime
* Cast
* Directors
* Overviews
* Trailer information

The imported data is stored in the application's database, allowing Django ORM queries to efficiently retrieve and organize the content.

The catalog can also be expanded through the TMDb import management command.

---

# 🔐 Authentication

VibeStream includes a user authentication system built using Django authentication and Django Allauth.

### Authentication Features

* User registration
* Username/email login
* Password authentication
* Logout
* Google OAuth
* Profile management
* Account deletion
* Personalized watchlist
* User-specific viewing progress

Authentication allows VibeStream to provide personalized features instead of treating every visitor as the same user.

---

# ❤️ Personal Watchlist

Authenticated users can save movies and TV shows to their personal watchlist.

Each watchlist is associated with the corresponding Django user.

```text
User
 │
 ├── Movie A
 ├── Movie B
 ├── TV Show A
 └── TV Show B
```

This provides a persistent **My List** experience across sessions.

---

# ▶️ Continue Watching

VibeStream includes viewing-progress tracking so users can continue content from where they previously stopped.

The system stores progress against the authenticated user and content item, allowing the application to retrieve the user's previously watched content.

This creates the foundation for a more complete streaming-style experience.

---

# 📊 Content Discovery

The home page organizes the catalog into multiple discovery sections.

### Movies

* 🔥 Trending Movies
* 🏆 Top Movies
* 🎭 Now Playing
* 📅 Upcoming Movies

### TV

* 📺 Trending TV Shows
* ⭐ Top Series

### Additional Discovery

* 🎭 Genre-based sections
* 🔎 Search results
* 🎬 Featured hero content
* ❤️ Personal watchlist
* ▶️ Continue Watching

The interface uses horizontal content rows and interactive navigation to create a streaming-platform-style browsing experience.

---

# 🛠️ Tech Stack

## 💻 Backend

| Technology         | Purpose                         |
| ------------------ | ------------------------------- |
| **Python 3.11**    | Core programming language       |
| **Django 5.2**     | Web framework                   |
| **Django ORM**     | Database interaction            |
| **Django Allauth** | Authentication and Google OAuth |
| **Gunicorn**       | Production WSGI server          |
| **WhiteNoise**     | Static file serving             |

---

## 🗄️ Database

| Technology          | Purpose                                |
| ------------------- | -------------------------------------- |
| **PostgreSQL**      | Production database                    |
| **SQLite**          | Local development database             |
| **dj-database-url** | Database URL configuration             |
| **Django ORM**      | Database querying and model management |

---

## 🤖 Data & Machine Learning

| Technology                   | Purpose                                           |
| ---------------------------- | ------------------------------------------------- |
| **TMDb API**                 | Movie and TV metadata                             |
| **Python Requests**          | API communication                                 |
| **Pandas**                   | Data processing                                   |
| **Scikit-learn**             | Machine learning and recommendation functionality |
| **Content-based techniques** | Finding relevant content based on metadata        |

---

## 🎨 Frontend

| Technology               | Purpose                             |
| ------------------------ | ----------------------------------- |
| **Django Templates**     | Server-rendered frontend            |
| **HTML5**                | Page structure                      |
| **CSS3**                 | Styling and responsive interface    |
| **JavaScript**           | Interactive functionality           |
| **Video.js**             | Video player functionality          |
| **HLS.js / HLS support** | Streaming-oriented playback support |

---

## ☁️ Deployment

| Service        | Purpose                                |
| -------------- | -------------------------------------- |
| **Render**     | Production web hosting                 |
| **PostgreSQL** | Production database                    |
| **Gunicorn**   | Application server                     |
| **WhiteNoise** | Static asset delivery                  |
| **GitHub**     | Source control and deployment workflow |

---

# 📁 Project Structure

```text
VibeStream/
│
├── accounts/
│   ├── views.py
│   ├── models.py
│   ├── backends.py
│   └── ...
│
├── movies/
│   │
│   ├── management/
│   │   └── commands/
│   │       └── import_tmdb.py
│   │
│   ├── templates/
│   │   └── movies/
│   │       ├── home.html
│   │       ├── tv.html
│   │       ├── favorites.html
│   │       ├── profile.html
│   │       └── ...
│   │
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
├── templates/
│
├── static/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 📦 Key Modules

```text
⭐ TMDb Data Importer
   Imports movie and TV metadata from the TMDb API.

⭐ Content Catalog
   Stores movie and TV information using Django models.

⭐ Search & Filtering
   Allows users to find content using different search parameters.

⭐ Recommendation System
   Uses content metadata and machine-learning techniques to identify
   relevant content.

⭐ Authentication System
   Handles registration, login, logout, Google OAuth and account management.

⭐ Watchlist System
   Stores user-specific movies and TV shows for later viewing.

⭐ Continue Watching
   Tracks viewing progress for authenticated users.

⭐ Content Discovery
   Organizes content into trending, top-rated, upcoming and category sections.

⭐ Deployment Configuration
   Supports production deployment with PostgreSQL, Gunicorn and WhiteNoise.
```

---

# 🗄️ Core Data Model

The main `Movie` model is designed to represent both movies and TV shows.

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

The `media_type` field distinguishes between:

```text
movie
tv
```

This allows a common content model to support both movies and television content while keeping the application architecture relatively simple.

---

# ⚙️ Local Development

## 1. Clone the repository

```bash
git clone https://github.com/prachi912/VibeStream.git
cd VibeStream
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

---

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
venv\Scripts\Activate.ps1
```

---

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure environment variables

Create a `.env` file in the project root.

```env
SECRET_KEY=your_secret_key
DEBUG=True

TMDB_API_KEY=your_tmdb_api_key

YOUTUBE_API_KEY=your_youtube_api_key

GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

DATABASE_URL=your_database_url
```

> ⚠️ Never commit `.env` files, API keys, OAuth secrets, or database credentials to GitHub.

---

## 6. Run migrations

```bash
python manage.py migrate
```

---

## 7. Import content

```bash
python manage.py import_tmdb
```

---

## 8. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# ☁️ Deployment

VibeStream is deployed using **Render**.

The deployment workflow is:

```text
GitHub Repository
        │
        ▼
     Render
        │
        ├── Gunicorn
        │
        ├── Django
        │
        ├── WhiteNoise
        │
        └── PostgreSQL
```

### Production Build Command

```bash
pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
```

### Production Start Command

```bash
gunicorn config.wsgi:application
```

Production secrets and environment variables are configured through the Render dashboard instead of being committed to the repository.

---

# 🔑 Environment Variables

| Variable               | Purpose                      |
| ---------------------- | ---------------------------- |
| `SECRET_KEY`           | Django security key          |
| `DEBUG`                | Development/production mode  |
| `TMDB_API_KEY`         | TMDb API authentication      |
| `YOUTUBE_API_KEY`      | YouTube API access           |
| `GOOGLE_CLIENT_ID`     | Google OAuth client ID       |
| `GOOGLE_CLIENT_SECRET` | Google OAuth secret          |
| `DATABASE_URL`         | PostgreSQL connection string |
| `ALLOWED_HOSTS`        | Allowed application hosts    |

> 🔒 **Security:** Never commit environment variables containing secrets to GitHub.

---

# 🧪 Current Production Data

The production database contains a mixed movie and TV catalog populated through the TMDb import process.

```text
Movies: 428+
TV Shows: 339+

Total Content: 767+
```

The catalog can be expanded further by importing additional TMDb content.

> Counts may change as the production catalog is updated.

---

# 🧩 Engineering Challenges & Decisions

## SQLite → PostgreSQL

SQLite was used during local development because it is lightweight and requires no separate database server.

For production, VibeStream uses PostgreSQL through `DATABASE_URL`.

This provides a more appropriate database setup for a deployed application.

---

## Local Database ≠ Production Database

The local SQLite database and Render PostgreSQL database are separate environments.

Therefore:

```text
Local SQLite
     ≠
Render PostgreSQL
```

Data imported into the local database does not automatically appear in production.

The TMDb import process can be executed against the appropriate environment to populate the production catalog.

---

## Django Templates Instead of React

VibeStream uses Django's server-rendered templates rather than introducing a separate React frontend.

This decision keeps the architecture relatively simple while still allowing:

* JavaScript interactions
* Dynamic carousels
* Interactive UI components
* Responsive CSS
* Video playback functionality

For this project's scope, Django provides both backend and frontend rendering without requiring a separate frontend deployment.

---

## External API Data Management

Instead of hardcoding movie information into templates, VibeStream retrieves content from TMDb and stores relevant metadata in the application's database.

This creates a workflow closer to a real data-driven application:

```text
TMDb API
   │
   ▼
Data Ingestion
   │
   ▼
Django Models
   │
   ▼
PostgreSQL
   │
   ▼
Django ORM
   │
   ▼
Web Application
```

---

# 🗺️ Roadmap

## ✅ Completed

* [x] Movie discovery
* [x] TV show discovery
* [x] TMDb API integration
* [x] Database-backed content catalog
* [x] User authentication
* [x] Google OAuth
* [x] Watchlist / My List
* [x] Continue Watching
* [x] Search and filtering
* [x] Trending hero carousel
* [x] Category-based content discovery
* [x] PostgreSQL production database
* [x] Responsive streaming-style interface
* [x] Render deployment

## 🚀 Planned Improvements

* [ ] Improved personalized recommendations
* [ ] More advanced recommendation models
* [ ] Expanded semantic search capabilities
* [ ] Improved video streaming pipeline
* [ ] More detailed viewing analytics
* [ ] Larger content catalog
* [ ] Performance optimization for large datasets
* [ ] Advanced content filtering
* [ ] Improved recommendation accuracy
* [ ] Better TV show and episode-level support

---

# 📈 What I Learned

Building VibeStream gave me hands-on experience with several practical software and data engineering concepts:

* Building a full-stack Django application
* Designing database models for movie and TV data
* Integrating a third-party REST API
* Building a data ingestion workflow
* Working with Django ORM and database queries
* Processing and organizing external API data
* Implementing authentication and OAuth
* Building user-specific features
* Working with machine-learning concepts for recommendations
* Managing environment variables and application secrets
* Working with SQLite during development
* Migrating to PostgreSQL for production
* Configuring Gunicorn for deployment
* Serving static files with WhiteNoise
* Debugging deployment and production issues
* Deploying a Django application on Render
* Using Git and GitHub for source control

---

# 🔮 Future Improvements

The long-term goal is to evolve VibeStream from a content discovery application into a more personalized data-driven platform.

A future recommendation pipeline could look like:

```text
                 User Activity
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
     Watchlist    Watch History   Search
          │           │           │
          └───────────┼───────────┘
                      ▼
              Feature Extraction
                      │
                      ▼
            Recommendation Engine
                      │
                      ▼
             Personalized Content
```

This could eventually combine content similarity with user behavior to produce more personalized recommendations.

---

# 🚀 Project Goals

VibeStream was built as a practical project to explore how a real-world content platform can combine:

```text
External Data
      +
Database
      +
Backend
      +
Search
      +
Machine Learning
      +
Authentication
      +
Cloud Deployment
```

The project also provided hands-on experience in taking an application from local development through production deployment.

---

# 👩‍💻 Author

<div align="center">

### Prachi Chauhan

**Computer Science Postgraduate | Aspiring Data Engineer**

Building with:

**Python • SQL • Data Engineering • ETL • Cloud • AI/ML**

<br>

<a href="https://github.com/prachi912">
  <img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github" alt="GitHub Profile">
</a>

<a href="https://www.linkedin.com/in/prachi-chauhan-79a446226">
  <img src="https://img.shields.io/badge/LinkedIn-Profile-0A66C2?style=for-the-badge&logo=linkedin" alt="LinkedIn Profile">
</a>

</div>

---

<div align="center">

### ⭐ If you find VibeStream interesting, consider giving the repository a star.

**Live Demo:**
https://vibestream-0k2c.onrender.com

**GitHub:**
https://github.com/prachi912/VibeStream

<br>

*Built with Python, Django, SQL, APIs, and a lot of debugging.*

</div>
