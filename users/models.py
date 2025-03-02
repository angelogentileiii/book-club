from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserProfileManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)  # Encrypt the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class UserProfile(AbstractBaseUser):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=1024)
    email_address = models.EmailField(unique=True)
    phone_number = PhoneNumberField(blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    favorited_books = models.ManyToManyField(
        "books.Book", related_name="favorited_by", blank=True
    )
    friends = models.ManyToManyField("self", symmetrical=True, blank=True)

    objects = UserProfileManager()

    # This is the field users will use to log in
    USERNAME_FIELD = "email_address"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
