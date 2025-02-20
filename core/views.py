from django.shortcuts import render
from django.views import View
from django.core.cache import cache
from django.utils.text import Truncator

from os import getenv
from datetime import datetime, timedelta

import requests
import json

fields = (
    "kind,totalItems,items(id,selfLink,volumeInfo/title, volumeInfo/subtitle, volumeInfo/authors, volumeInfo/publisher, volumeInfo/publishedDate, volumeInfo/description, volumeInfo/industryIdentifiers, volumeInfo/categories, volumeInfo/imageLinks, volumeInfo/previewLink)",
)

params = {
    "key": getenv("GOOGLE_API_KEY"),
    "maxResults": 10,
    "orderBy": "newest",
    "printType": "books",
    "langRestrict": "en",
    "fields": fields,
}


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
                url = f"https://www.googleapis.com/books/v1/volumes"
                params["q"] = f"subject:{genre}"

                response = requests.get(url, params=params)

                if response.status_code == 200:
                    data = response.json()
                    all_books = data.get("items", [])
                    filtered_books = newest_books_filter(all_books)

                    genre_books = filtered_books[:2]  # Limit to first 10 books

                    for book in genre_books:
                        description = book["volumeInfo"].get("description", "")
                        truncated_description = Truncator(description).words(75)
                        book["volumeInfo"][
                            "truncated_description"
                        ] = truncated_description

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


#########################################################################################################################################
# ATTEMPT TO WORK WITH ISBN API --> No manner to retrieve recent publications

# ISBN_KEY = getenv("ISBN_API_KEY")

# url = "https://api2.isbndb.com/search/books"
# headers = {"accept": "application/json", "Authorization": ISBN_KEY}

# params = {
#     "subject": "fiction",
#     "page": 1,
#     "pageSize": 35,
# }

# response = requests.get(url, headers=headers, params=params)

# # If the response is successful, process the data
# if response.status_code == 200:
#     books = response.json()

#     print(json.dumps(books, indent=2))

#     # Check if the 'data' field is in the response and process the books
#     fiction_books = books.get("data", [])

#     if fiction_books:
#         fiction_books = fiction_books[:5]

#     if not fiction_books:
#         fiction_books = [{"title": "No books found in this genre."}]
# else:
#     fiction_books = [
#         {"title": f"Error: {response.status_code} - Unable to fetch books."}
#     ]
#     print(f"Error Code: {response.status_code} - {response.text}")

# # Return the context with books (or error message)
# return render(request, self.template_name, {"fiction_books": fiction_books})
