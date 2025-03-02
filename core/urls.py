from django.urls import path
from .views import HomePageView, SearchBooksView

urlpatterns = [
    path("", HomePageView.as_view(), name="home_page"),
    path("search/", SearchBooksView.as_view(), name="search_books"),
]
