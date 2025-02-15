from django.contrib import admin
from .models import BookClub, PastBook, Membership

# Register your models here.


@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ("__str__", "current_book")
    list_filter = ("name",)
