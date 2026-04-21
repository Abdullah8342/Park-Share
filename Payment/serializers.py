from rest_framework import serializers
from .models import Payment


class PaymentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id','user','reservation_id','status','amount','paid_at']
        read_only = ['id','amount','paid_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
