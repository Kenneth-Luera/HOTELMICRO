from rest_framework.permissions import BasePermission
from .models import Hotel

class IsHotelOwner(BasePermission):

    def has_permission(self, request, view):

        print("AUTH:", request.auth)

        if not request.auth:
            return False

        try:
            return request.auth['role'] == 'hotel'
        except Exception:
            return False

class IsRoomOwner(BasePermission):

    def has_permission(self, request, view):

        if not request.auth:
            return False

        if request.auth['role'] != 'hotel':
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.hotel.owner_id == request.user.id