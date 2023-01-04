from rest_framework import serializers
from django.contrib.auth import get_user_model
from hotel_manager.users.models import Hotel, HotelRoom

User = get_user_model()


class HotelSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(required=True)
    # description = serializers.CharField(required=False)
    # offer = serializers.CharField(required=False)
    # country = serializers.CharField(required=False)

    # # def validate(self, attrs):
    # #     hotel = Hotel.objects.filter(name=attrs['name']).first()
    # #     if hotel:
    # #         raise serializers.ValidationError({"error": "HOTEL_NAME_USED"})
    # #     return attrs

    # # def create(self, validated_data):
    # #     hotel = Hotel.objects.create(
    # #         name=validated_data.get('name'),
    # #         description=validated_data.get('description'),
    # #         offer=validated_data.get('offer'),
    # #         country=validated_data.get('country'),
    # #         rate_hotel=validated_data.get('rate_hotel'),
    # #     )
    # #     hotel.save()
    # #     return hotel

    class Meta:
        model = Hotel
        fields = '__all__'


class HotelRoomSerializer(serializers.ModelSerializer):
    # hotel_id = serializers.IntegerField(required=True)
    # room_code = serializers.CharField(required=True)
    # name = serializers.CharField(required=False)
    # offer = serializers.IntegerField(required=False)    
    # description = serializers.CharField(required=False)
    # price = serializers.FloatField(required=True)

    # def validate(self, attrs):
    #     _room = HotelRoom.objects.filter(room_code=attrs['room_code'])
    #     if not _room:
    #         raise serializers.ValidationError({"error": "ROOM_IS_EXIST"})
    #     return attrs

    # def create(self, validated_data):
    #     _hotel = Hotel.objects.filter(id=validated_data.get('hotel_id')).first()
    #     if not _hotel:
    #         raise serializers.ValidationError({"error": "HOTEL_IS_NOT_EXIST"})
    #     room = HotelRoom.objects.create(
    #         hotel_id=_hotel,
    #         room_code=validated_data.get('room_code'),
    #         name=validated_data.get('name'),
    #         description=validated_data.get('description'),
    #         offer=validated_data.get('offer'),
    #         price=validated_data.get('price'),
    #         image = validated_data.get('image')
    #     )
    #     room.save()
    #     return room

    class Meta:
        model = HotelRoom
        fields = '__all__'
