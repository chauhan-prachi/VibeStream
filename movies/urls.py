from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    
    path("search/", views.search, name="search"),
    path("categories/", views.categories_page, name="categories"),
    path("tv/", views.tv_page, name="tv"),
    path("favorites/", views.favorites_page, name="favorites"),
    path("profile/", views.profile_page, name="profile"),

    path("watchlist/add/<int:movie_id>/", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist/remove/<int:movie_id>/", views.remove_from_watchlist, name="remove_from_watchlist"),

    path("continue-watching/remove/<int:movie_id>/", views.remove_from_continue_watching, name="remove_from_continue_watching"),

    path("watchlist/", views.watchlist_page, name="watchlist"),
    path("continue-watching/", views.continue_watching_page, name="continue_watching"),

    path("movie/<int:movie_id>/", views.movie_detail, name="movie_detail"),
    path("watch/<int:movie_id>/", views.watch_movie, name="watch_movie"),
    path("progress/<int:movie_id>/", views.save_progress, name="save_progress"),
    path("watchlist/toggle/<int:movie_id>/",views.toggle_watchlist,name="toggle_watchlist",),
]