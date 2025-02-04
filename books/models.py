from django.db import models
from reviews.models import Review


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    published_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True)
    genres = models.CharField(max_length=25)
    length = models.IntegerField()

    author = models.ManyToManyField(Author, related_name="authored_books")
    reviews = models.ManyToManyField(Review, related_name="reviewed_books")

    @property
    def average_rating(self):
        average = self.reviews.aggregate(models.Avg("rating"))["rating__avg"]
        if average is None:
            return "There are currently no reviews for this title"
        return round(average, 2)

    def __str__(self):
        return f"{self.title} by {', '.join([author.name for author in self.author.all()])}"
