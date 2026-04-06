from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import HotelSerializer
from .permissions import IsHotelOwner
from .models import Room, Hotel
from .serializers import RoomSerializer
from .permissions import IsRoomOwner
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404


class HotelViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [IsAuthenticated, IsHotelOwner]

    def get_queryset(self):
        if not self.request.auth:
            return Hotel.objects.none()

        user_id = self.request.auth.get('user_id')
        return Hotel.objects.filter(owner_id=user_id)

    def perform_create(self, serializer):
        if not self.request.auth:
            raise Exception("No autenticado")

        try:
            user_id = self.request.auth['user_id']
        except Exception:
            raise Exception("Token inválido")

        serializer.save(owner_id=user_id)

class RoomViewSet(viewsets.ModelViewSet):

    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsRoomOwner]

    def get_queryset(self):
        if not self.request.auth:
            return Room.objects.none()

        user_id = self.request.user.id

        return Room.objects.filter(hotel__owner_id=user_id)

    def perform_create(self, serializer):

        hotel = serializer.validated_data.get('hotel')

        print("HOTEL OWNER:", hotel.owner_id)
        print("USER ID:", self.request.user.id)

        if str(hotel.owner_id) != str(self.request.user.id):
            raise PermissionDenied("No puedes agregar habitaciones a este hotel")

        serializer.save()

    @action(detail=True, methods=['get'], url_path='internal')
    def internal_detail(self, request, pk=None):

        # no usar get_object() por que tiene permisos y queremos omitirlos para esta parte
        room = get_object_or_404(Room, id=pk)

        return Response({
            "id": str(room.id),
            "price_per_night": room.price_per_night
        })

    def get_permissions(self):

        if self.action == 'internal_detail':
            return [AllowAny()]

        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]

        return [IsAuthenticated(), IsRoomOwner()]