from django.contrib import admin
from .models import ChatRoom

# Register your models here.


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_members")

    def get_members(self, obj):
        users = obj.members.all()
        return ", ".join(user.__str__() for user in users)

    get_members.short_description = "Members"
