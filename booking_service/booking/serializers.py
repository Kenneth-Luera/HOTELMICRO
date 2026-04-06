from rest_framework import serializers
from .models import Booking
from datetime import date

class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ('user_id', 'total_price')

    def validate(self, data):

        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Fechas inválidas")

        if data['check_in'] < date.today():
            raise serializers.ValidationError("No puedes reservar en el pasado")

        return data