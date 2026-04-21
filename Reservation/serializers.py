'''
    Reservation Serializer
'''
from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from .models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    '''
        Reservation Serializer
    '''
    class Meta:
        '''
            Meta
        '''
        model = Reservation
        fields = [
            "id",
            "parking_spot",
            "vehicle_type",
            "driver",
            "start_time",
            "end_time",
            "total_price",
            "status",
            "created_at",
        ]
        read_only_fields = ['id','driver','total_price']


    def validate(self, attrs):
        start_time = attrs.get('start_time', getattr(self.instance, 'start_time', None))
        end_time = attrs.get('end_time', getattr(self.instance, 'end_time', None))
        now = timezone.now()
        min_start_time = now + timedelta(minutes=5)

        if start_time and start_time < now:
            raise serializers.ValidationError({
                'start_time': 'Start time cannot be in the past.'
            })

        if start_time and start_time < min_start_time:
            raise serializers.ValidationError({
                'start_time': 'Start time must be at least 5 minutes from now.'
            })

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError({
                'end_time': 'End time must be after start time.'
            })

        return attrs

    def create(self, validated_data):
        print("Reservation Serializer Create")
        validated_data['driver'] = self.context['request'].user
        return super().create(validated_data)
