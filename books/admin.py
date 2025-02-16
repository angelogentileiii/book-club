from django.contrib import admin
from .models import Book, Author, Review

# Register your models here.


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "get_author",
        "published_date",
        "isbn",
        "length",
        "average_rating",
    )

    readonly_fields = ("average_rating",)

    def get_author(self, obj):
        authors = obj.author.all()
        return ", ".join(author.name for author in authors)

    get_author.short_description = "Author(s)"


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "get_books")

    def get_books(self, obj):
        books = obj.authored_books.all()
        return ", ".join([book.title for book in books])

    get_books.short_description = "Books"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("get_user", "get_book", "rating", "short_comment")

    def get_user(self, obj):
        return obj.user

    def get_book(self, obj):
        return obj.book.title

    def short_comment(self, obj):
        return obj.comment[:25]

    get_user.short_description = "User"
    get_book.short_description = "Book"
    short_comment.short_description = "Comment"
