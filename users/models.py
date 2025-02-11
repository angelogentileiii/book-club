from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.


class UserProfile(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    email_address = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True)

    favorited_books = models.ManyToManyField(
        "books.Book", related_name="favorited_by", blank=True
    )
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
