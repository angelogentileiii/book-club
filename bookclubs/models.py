from django.db import models
from books.models import Book
from users.models import UserProfile

from django.core.exceptions import ValidationError

# Create your models here.


class BookClub(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    VISIBILITY_CHOICES = [(PUBLIC, "public"), (PRIVATE, "private")]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)
    current_book = models.ForeignKey(
        Book, on_delete=models.SET_NULL, null=True, blank=True, related_name="bookclubs"
    )
    visibility = models.CharField(
        max_length=25, choices=VISIBILITY_CHOICES, default=PUBLIC
    )

    def __str__(self):
        return f"{self.name} ({self.visibility})"


class Membership(models.Model):
    ADMIN = "admin"
    MEMBER = "member"
    ROLES = [(ADMIN, "Admin"), (MEMBER, "Member")]

    user = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="memberships"
    )
    bookclub = models.ForeignKey(
        BookClub, on_delete=models.CASCADE, related_name="members"
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLES, default=MEMBER)

    class Meta:
        unique_together = ("user", "bookclub")  # Prevents duplicate memberships

    def __str__(self):
        return f"{self.user} - {self.bookclub} ({self.role})"

    def validate_admin_count(self, bookclub):
        admin_count = Membership.objects.filter(
            bookclub=bookclub, role=Membership.ADMIN
        ).count()

        if admin_count < 1:
            raise ValidationError(
                "Each book club must have at least one admin. Please set a new admin."
            )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.validate_admin_count(self.bookclub)

    def delete(self, *args, **kwargs):
        if self.role == Membership.ADMIN:
            self.validate_admin_count(self.bookclub)
        super().delete(*args, **kwargs)
