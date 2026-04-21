from rest_framework import serializers
from .models import (
    Location,
    VehicleTypeSpported,
    Organization,
    ParkingSpot
)


class LocationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Location
        fields = ["id","owner", "country", "city", "area", "description"]
        read_only_fields = ['id','owner']


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)




class VehicleTypeSpportedSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = VehicleTypeSpported
        fields = ["id", "owner", "vehicle_type", "price_per_hour"]
        read_only_fields = ['id','owner']



    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)



class OrganizationSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only = True)
    class Meta:
        model = Organization
        fields = [
            "id",
            "owner",
            "name",
            "city",
            "created_at",
        ]
        read_only_fields = ['id','owner','created_at']


    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)



class ParkingSpotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSpot
        fields = ["id", "title", "description","organization","location","vehicle_supported", "status"]
