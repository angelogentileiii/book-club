def genre_list(request):
    return {
        "genres": [
            "fiction",
            "mystery",
            "fantasy",
            "romance",
            "science fiction",
            "non-fiction",
            "crime",
            "all-genres",
        ]
    }
