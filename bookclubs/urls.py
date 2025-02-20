from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path("bookclubs/", views.BookClubsView.as_view(), name="book-clubs"),
]
