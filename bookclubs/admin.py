from django.contrib import admin
from .models import BookClub, PastBook, Membership


# Register your models here.
@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = (
        "__str__",
        "current_book",
        "get_members",
        "visibility",
        "creator",
        "get_past_books",
    )
    list_filter = ("name",)

    def get_members(self, obj):
        members = obj.members.all()
        return ", ".join(str(member.user) for member in members)

    def get_past_books(self, obj):
        past_books = obj.past_books.all()
        return ", ".join(str(past_book.book) for past_book in past_books)

    get_members.short_description = "Members"
    get_past_books.short_description = "Past Books"

    @admin.register(Membership)
    class MembershipAdmin(admin.ModelAdmin):
        list_display = ("user", "bookclub", "role")
        list_filter = ("role", "bookclub")

    @admin.register(PastBook)
    class PastBookAdmin(admin.ModelAdmin):
        list_display = ("book", "bookclub")
        list_filter = ("bookclub", "book")
