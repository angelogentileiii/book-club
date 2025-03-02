from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path("", views.BookClubsView.as_view(), name="book_clubs"),
]
