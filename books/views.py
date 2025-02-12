from django.shortcuts import render
from django.views import View

from os import getenv

import requests
import random
import json


# Create your views here.
class HomePageView(View):
    template_name = "books/index.html"

    def get(self, request, *args, **kwargs):
        API_KEY = getenv("GOOGLE_API_KEY")
        query = "fiction"
        max_results = 40

        # url = "https://openlibrary.org/search.json?q=book&limit=6"  # Fetch more books for randomness
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&key={API_KEY}&maxResults={max_results}"
        response = requests.get(url)

        books = []
        if response.status_code == 200:
            data = response.json()
            # all_books = data.get("docs", [])
            all_books = data.get("items", [])
            books = random.sample(
                all_books, min(len(all_books), 6)
            )  # Get up to 6 random books

        print(json.dumps(books, indent=2))

        return render(request, self.template_name, {"books": books})
