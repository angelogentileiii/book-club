from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path("<str:book_id>", views.BookDetailView.as_view(), name="book-detail"),
]
