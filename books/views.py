from django.shortcuts import render, get_object_or_404
from django.views import View

from os import getenv

import requests


# Create your views here.
class BookDetailView(View):
    template_name = "books/book-detail.html"

    def get(self, request, *args, **kwargs):
        book_id = kwargs["book_id"]

        # Fetch the book details from session
        book_details = request.session.get(f"book_{book_id}")

        if not book_details:
            # If not cached in session, make a fresh request
            url = f"https://www.googleapis.com/books/v1/volumes/{book_id}"
            params = {"key": getenv("GOOGLE_API_KEY")}
            response = requests.get(url, params=params)

            if response.status_code == 200:
                book_details = response.json()
                # Cache the result in session for future use
                request.session[f"book_{book_id}"] = book_details
            else:
                book_details = {"error": f"Error fetching details for book {book_id}"}

        return render(request, self.template_name, {"book_details": book_details})
