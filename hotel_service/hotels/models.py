import uuid
from django.db import models

class Hotel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner_id = models.UUIDField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['owner_id', 'name'],
                name='unique_hotel_per_owner'
            )
        ]

class Room(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    hotel = models.ForeignKey(
        'Hotel',
        on_delete=models.CASCADE,
        related_name='rooms'
    )

    number = models.CharField(max_length=10)  # Ej: 101, A1
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['hotel', 'number'],
                name='unique_room_per_hotel'
            )
        ]

    def __str__(self):
        return f"{self.hotel.name} - Room {self.number}"