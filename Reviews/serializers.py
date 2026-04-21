from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    '''
        Review Serializer
    '''

    class Meta:
        model = Review
        fields = [
            'id',
            'parking_spot',
            'reviewer',
            'rating',
            'comment',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'reviewer', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['reviewer'] = self.context['request'].user
        return super().create(validated_data)
