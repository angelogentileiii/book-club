from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from os import getenv
from datetime import datetime, timedelta

import requests

params = {
    "key": getenv("GOOGLE_API_KEY"),
    "maxResults": 40,
    "orderBy": "newest",
    "printType": "books",
    "langRestrict": "en",
}


# Create your views here.
class HomePageView(View):
    template_name = "core/index.html"

    def get(self, request, *args, **kwargs):

        current_date = datetime.now()
        two_months_ago = current_date - timedelta(days=90)
        start_date = two_months_ago.strftime("%Y-%m-%d")
        end_date = current_date.strftime("%Y-%m-%d")

        fiction_books = cache.get("fiction_books")

        if not fiction_books:
            url = f"https://www.googleapis.com/books/v1/volumes"
            params["q"] = "subject:Fiction"

            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                all_books = data.get("items", [])

                filtered_books = []
                for book in all_books:
                    published_date = book.get("volumeInfo", {}).get("publishedDate", "")
                    try:
                        if published_date:
                            # Check if the published date is within the last 2 months
                            published_date_obj = datetime.strptime(
                                published_date, "%Y-%m-%d"
                            )
                            if (
                                start_date
                                <= published_date_obj.strftime("%Y-%m-%d")
                                <= end_date
                            ):
                                filtered_books.append(book)
                    except ValueError:
                        pass  # Ignore invalid date formats

                fiction_books = filtered_books[:10]  # Limit to first 10 books
                cache.set("fiction_books", fiction_books, timeout=3600)
            else:
                fiction_books = [
                    {"title": f"Error: {response.status_code} - Unable to fetch books."}
                ]
                print(f"Error Code: {response.status_code} - {response.text}")
        else:
            print("Loaded fiction books from cache.")

        return render(request, self.template_name, {"fiction_books": fiction_books})

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
