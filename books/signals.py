from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Review, Book


# Update the average rating when a new review is created or deleted
@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def update_book_average_rating(sender, instance, **kwargs):
    book = instance.book
    book.update_average_rating()
