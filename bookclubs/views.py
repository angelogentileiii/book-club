from django.shortcuts import render
from django.views.generic import ListView

from .models import BookClub


# Create your views here.
class BookClubsView(ListView):
    model = BookClub
    template_name = "bookclubs/bookclubs.html"
    context_object_name = "bookclubs"
    ordering = ["name"]
