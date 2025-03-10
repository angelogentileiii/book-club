from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.core.cache import cache
from django.utils.text import Truncator

from os import getenv
from datetime import datetime, timedelta

import requests
import json

fields = (
    "kind,totalItems,items(id,selfLink,volumeInfo/title, volumeInfo/subtitle, volumeInfo/authors, volumeInfo/publisher, volumeInfo/publishedDate, volumeInfo/description, volumeInfo/industryIdentifiers, volumeInfo/categories, volumeInfo/imageLinks, volumeInfo/previewLink, volumeInfo/infoLink)",
)

params = {
    "key": getenv("GOOGLE_API_KEY"),
    "maxResults": 10,
    "printType": "books",
    "langRestrict": "en",
    "fields": fields,
    "projection": "full",
}

url = f"https://www.googleapis.com/books/v1/volumes"


# Create your views here.
class HomePageView(View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):
        genres = [
            "Fiction",
            "Nonfiction",
            "History",
            "Religion",
            "Travel",
            "Historical+Fiction",
        ]
        books_by_genre = {}

        for genre in genres:
            cache_key = f"{genre.lower()}_books"
            genre_books = cache.get(cache_key)

            if not genre_books:
                params["q"] = f"subject:{genre}"
                params["orderBy"] = "newest"

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    all_books = data.get("items", [])
                    filtered_books = newest_books_filter(all_books)

                    genre_books = filtered_books[:2]

                    truncate_description(genre_books)

                    cache.set(
                        cache_key, genre_books, timeout=3600
                    )  # Cache books for 1 hour
                else:
                    genre_books = [
                        {
                            "title": f"Error: {response.status_code} - Unable to fetch books for {genre}."
                        }
                    ]

                    print(f"Error Code: {response.status_code} - {response.text}")

            if "+" in genre:
                genre = genre.replace("+", " ")

            books_by_genre[genre] = genre_books

            print(json.dumps(books_by_genre, indent=2))

        return render(request, self.template_name, {"books_by_genre": books_by_genre})


class SearchBooksView(ListView):
    template_name = "core/search.html"
    context_object_name = "books"

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        search_type = self.request.GET.get("search_type", "title")
        searched_books = []

        if query:
            match search_type:
                case "author":
                    query = f"inauthor:{query}"
                case "title":
                    query = f"intitle:{query}"
                case "isbn":
                    query = f"isbn:{query}"
                case _:
                    query = f"intitle:{query}"

            params["q"] = query
            params["orderBy"] = "relevance"
            response = requests.get(url, params)

            if response.status_code == 200:
                data = response.json()
                searched_books = data.get("items", [])

                # Ensure that results only include populated data --> Necessary items are not missing
                searched_books = [
                    book
                    for book in searched_books
                    if book.get("volumeInfo")
                    and book["volumeInfo"].get("title")
                    and book["volumeInfo"].get("authors")
                    and book["volumeInfo"].get("publishedDate")
                    and book["volumeInfo"].get("imageLinks")
                    and book["volumeInfo"].get("description")
                ]

                # Allow for description preview
                truncate_description(searched_books)

        return searched_books

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context


def truncate_description(books):
    for book in books:
        description = book["volumeInfo"].get("description", "")

        word_count = sum(1 for word in description.split() if word)

        # Check if description length is greater than 65 characters
        if word_count > 65:
            truncated_description = Truncator(description).words(65)
            book["volumeInfo"]["truncated_description"] = truncated_description
            book["volumeInfo"]["is_truncated"] = True  # Flag to indicate truncation
        else:
            book["volumeInfo"]["is_truncated"] = False  # No truncation needed

    return books


def newest_books_filter(books):
    current_date = datetime.now()
    two_months_ago = current_date - timedelta(days=90)
    start_date = two_months_ago.strftime("%Y-%m-%d")
    end_date = current_date.strftime("%Y-%m-%d")

    filtered_books = []

    for book in books:
        published_date = book.get("volumeInfo", {}).get("publishedDate", "")
        try:
            if published_date:
                # Check if the published date is within the last 2 months
                published_date_obj = datetime.strptime(published_date, "%Y-%m-%d")
                if start_date <= published_date_obj.strftime("%Y-%m-%d") <= end_date:
                    filtered_books.append(book)
        except ValueError:
            pass  # Ignore invalid date formats

    return filtered_books
