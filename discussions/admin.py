from django.contrib import admin
from .models import DiscussionQuestion


# Register your models here.
@admin.register(DiscussionQuestion)
class DiscussionQuestionAdmin(admin.ModelAdmin):
    list_display = ("__str__", "get_user")

    def get_user(self, obj):
        return obj.asked_by

    get_user.short_description = "Asked By"
