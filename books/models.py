from django.db import models
from django.db.models import Avg

# Create your models here.


# Class for storing Authors in our database --> Very rough framework (02/14)
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)


# Class for our Books in our database
class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    description = models.TextField(max_length=500, blank=True)
    genres = models.CharField(max_length=25)
    length = models.IntegerField()

    author = models.ManyToManyField("Author", related_name="authored_books")

    average_rating = models.DecimalField(
        max_digits=3, decimal_places=2, null=True, blank=True
    )

    # Helper to update the cumulative average rating pulled from all related reviews of the book
    def update_average_rating(self):
        reviews = self.reviews.all()
        if reviews.exists():
            average = reviews.aggregate(Avg("rating"))["rating__avg"]

            # Update the book's average_rating field
            self.average_rating = round(average, 2) if average else None
            self.save()
        else:
            # If there are no reviews, set average_rating to None
            self.average_rating = None
            self.save()

    def __str__(self):
        return f"{self.title} by {', '.join([author.name for author in self.author.all()])}"


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    book = models.ForeignKey("Book", on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=3,  # Allow up to 3 digits in total (e.g., 5.0 or 3.8)
        decimal_places=1,  # One decimal place for tenths (e.g., 4.7)
        # Rating must be between 0 and 5
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0),
        ],
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Prevents duplicate reviews by the same user
        unique_together = ("user", "book")

    def __str__(self):
        return f"{self.user.__str__} - {self.book.title} ({self.rating}/5)"
