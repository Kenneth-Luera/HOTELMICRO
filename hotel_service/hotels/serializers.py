from rest_framework import serializers
from .models import Hotel, Room

class HotelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hotel
        fields = '__all__'

    def validate(self, data):
        request = self.context['request']
        owner_id = request.user.id
        name = data.get('name')

        if Hotel.objects.filter(owner_id=owner_id, name=name).exists():
            raise serializers.ValidationError(
                "Ya tienes un hotel con ese nombre"
            )

        return data


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = '__all__'

    def validate(self, data):
        hotel = data.get('hotel')
        number = data.get('number')

        if Room.objects.filter(hotel=hotel, number=number).exists():
            raise serializers.ValidationError(
                "Esta habitación ya existe en el hotel"
            )

        return data