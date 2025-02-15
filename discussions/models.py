from django.db import models


# Create your models here.
class DiscussionQuestion(models.Model):
    past_book = models.ForeignKey(
        "bookclubs.PastBook", on_delete=models.CASCADE, related_name="questions"
    )
    question = models.TextField()
    asked_by = models.ForeignKey(
        "users.UserProfile", on_delete=models.SET_NULL, null=True, blank=True
    )
    asked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Discussion Question"
        verbose_name_plural = "Discussion Questions"

    def __str__(self):
        return f"Question for {self.past_book.book.title}: {self.question[:25]}"


class QuestionResponse(models.Model):
    question = models.ForeignKey(
        "DiscussionQuestion", on_delete=models.CASCADE, related_name="responses"
    )
    responded_by = models.ForeignKey(
        "users.UserProfile", on_delete=models.SET_NULL, null=True, blank=True
    )
    response = models.TextField()
    responded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Response by {self.responded_by} to {self.question}"
