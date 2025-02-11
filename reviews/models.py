from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey("users.UserProfile", on_delete=models.CASCADE)
    book = models.ForeignKey("books.Book", on_delete=models.CASCADE)
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
