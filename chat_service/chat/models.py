import uuid
from django.db import models

class Message(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    room_id = models.CharField(max_length=255)

    sender_id = models.CharField(max_length=255)
    sender_role = models.CharField(max_length=50)

    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_id}: {self.content}"