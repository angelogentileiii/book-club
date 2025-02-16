from django.contrib import admin
from .models import BookClub, PastBook, Membership


# Register your models here.
@admin.register(BookClub)
class BookClubAdmin(admin.ModelAdmin):
    list_display = ("__str__", "current_book", "get_members", "visibility", "creator")
    list_filter = ("name",)

    def get_members(self, obj):
        members = obj.members.all()
        return ", ".join(str(member.user) for member in members)

    get_members.short_description = "Members"

    @admin.register(Membership)
    class MembershipAdmin(admin.ModelAdmin):
        list_display = ("user", "bookclub", "role")
        list_filter = ("role", "bookclub")
