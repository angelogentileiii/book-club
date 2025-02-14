from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.


# Class for BookClubs --> Two Visibility Choices
class BookClub(models.Model):
    PUBLIC = "public"
    PRIVATE = "private"
    VISIBILITY_CHOICES = [(PUBLIC, "public"), (PRIVATE, "private")]

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500, blank=True)

    # Each club can only set one book as the current book at a time
    current_book = models.ForeignKey(
        "books.Book",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookclubs",
    )

    visibility = models.CharField(
        max_length=25, choices=VISIBILITY_CHOICES, default=PUBLIC
    )

    def __str__(self):
        return f"{self.name} ({self.visibility})"


# Class for storing all of the information from a PastBook --> Upon completion or change of current book
class PastBook(models.Model):
    bookclub = models.ForeignKey(
        "BookClub", on_delete=models.CASCADE, related_name="past_books"
    )

    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="past_clubs"
    )

    completion_date = models.DateField()

    # Rating will be a cumulative average from all ratings received by bookclub members
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)


# Class to register a User with a BookClub and their respective role
class Membership(models.Model):
    ADMIN = "admin"
    MEMBER = "member"
    ROLES = [(ADMIN, "Admin"), (MEMBER, "Member")]

    user = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="memberships"
    )

    bookclub = models.ForeignKey(
        "BookClub", on_delete=models.CASCADE, related_name="members"
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=ROLES, default=MEMBER)

    class Meta:
        # Prevents duplicate memberships within the book club
        unique_together = ("user", "bookclub")

    def __str__(self):
        return f"{self.user} - {self.bookclub} ({self.role})"

    # Helper method to ensure that every bookclub must have at least one Admin as a member
    def has_admin(self):
        return (
            Membership.objects.filter(bookclub=self.bookclub, role=Membership.ADMIN)
            .exclude(id=self.id)
            .exists()
        )

    # Ensures that we check for a currently existing admin to the bookclub before saving, we cannot save a Member first
    def save(self, *args, **kwargs):
        if self.role == Membership.MEMBER or not self.has_admin():
            raise ValidationError(
                "Each book club must have at least one admin. Please set a new admin."
            )
        super().save(*args, **kwargs)

    # Ensures that there will be an admin remaining before the role can be deleted (member removed from BookClub or changed to member role)
    def delete(self, *args, **kwargs):
        if self.role == Membership.ADMIN or not self.has_admin():
            raise ValidationError(
                "Cannot remove the last admin. Assign another admin to the book club first."
            )
        super().delete(*args, **kwargs)
