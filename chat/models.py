from django.db import models


# Create your models here.


# Class for Chatroom Model throughout app
class ChatRoom(models.Model):
    DIRECT = "direct"
    GROUP = "group"
    BOOKCLUB = "bookclub"

    CHAT_TYPES = [
        (DIRECT, "Direct"),
        (GROUP, "Group"),
        (BOOKCLUB, "BookClub"),
    ]

    name = models.CharField(max_length=255, blank=True, null=True)
    chat_type = models.CharField(max_length=10, choices=CHAT_TYPES)

    # Only for book club chats --> Otherwise null
    bookclub = models.ForeignKey(
        "bookclubs.BookClub",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="chatrooms",
    )

    participants = models.ManyToManyField("users.UserProfile", related_name="chatrooms")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name if self.name else f"Chat ({self.chat_type})"


# Class for ChatMessages to store chat histories
class ChatMessage(models.Model):
    sender = models.ForeignKey(
        "users.UserProfile", on_delete=models.CASCADE, related_name="messages"
    )

    # Store messages in relation to ChatRoom
    chatroom = models.ForeignKey(
        "ChatRoom", on_delete=models.CASCADE, related_name="messages"
    )

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} in {self.chatroom}: {self.content[:30]}"
