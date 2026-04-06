from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Booking
from .serializers import BookingSerializer
from datetime import timedelta
from .services import get_room


class BookingViewSet(viewsets.ModelViewSet):

    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):

        room_id = self.request.data.get('room_id')
        check_in = serializer.validated_data.get('check_in')
        check_out = serializer.validated_data.get('check_out')

        # 🔥 VALIDAR DISPONIBILIDAD
        overlapping = Booking.objects.filter(
            room_id=room_id,
            check_in__lt=check_out,
            check_out__gt=check_in
        ).exists()

        if overlapping:
            raise ValidationError("La habitación no está disponible en esas fechas")

        # 🔥 OBTENER ROOM REAL
        room = get_room(room_id)

        if not room:
            raise ValidationError("Habitación no encontrada")

        price_per_night = float(room['price_per_night'])

        # 🔥 CALCULAR TOTAL
        days = (check_out - check_in).days
        total = days * price_per_night

        serializer.save(
            user_id=self.request.user.id,
            room_id=room_id,
            total_price=total
        )