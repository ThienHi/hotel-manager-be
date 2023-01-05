from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from hotel_manager import constants
from hotel_manager.users.models import Hotel, HotelImage, HotelRoom, RoomImage
from hotel_manager.users.api.hotel_serializers import HotelSerializer,HotelRoomSerializer
# from hotel_manager.users.api.pagination_class import CustomPagination


class HotelImageViewSet(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user = request.user.id
        if user.user_type != constants.ADMIN:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        sz = HotelSerializer(data=request.data)
        if sz.is_valid(raise_exception = True):
            sz.save()
            hotel = Hotel.objects.get(id=sz.data.get('id'))
            images = request.FILES.getlist('file')
            for image in images:
                activity_image = HotelImage(hotel=hotel, image=image)
                activity_image.save()
        return Response(sz.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk, *args, **kwargs):
        user = request.user.id
        sz = HotelSerializer(data=request.data)
        if user.user_type != constants.ADMIN:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        if sz.is_valid(raise_exception = True):
            hotel = Hotel.objects.filter(id=pk).first()
            if not hotel:
                return Response("HOTEL_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
            hotel.name = sz.data.get('name')
            hotel.description = sz.data.get('description')
            hotel.name = sz.data.get('offer')
            hotel.country = sz.data.get('country')
            hotel.save()
            return Response("UPDATE_HOTEL_SUCCESS", status=status.HTTP_200_OK)

    def destroy(self, request, pk, *args, **kwargs):
        user = request.user.id
        if user.user_type != constants.ADMIN:
            return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
        hotel = Hotel.objects.filter(id=pk).first()
        if not hotel:
            return Response("HOTEL_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
        hotel.delete()
        return Response("DELETE_HOTEL_SUCCESS", status=status.HTTP_204_NO_CONTENT)


class HotelView(viewsets.ModelViewSet):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    permission_classes = [AllowAny]

    # def list(self, request, *args, **kwargs):
    #     hotel = Hotel.objects.all()
    #     paginator = self.pagination_class()
    #     page = paginator.paginate_queryset(hotel, request)
    #     serializer = HotelSerializer(page, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)


class HotelRoomViewSet(viewsets.ModelViewSet):
    queryset = HotelRoom.objects.all()
    serializer_class = HotelRoomSerializer
    permission_classes = [IsAuthenticated]

    # def list(self, request, *args, **kwargs):
    #     hotel = HotelRoom.objects.all()
    #     paginator = self.pagination_class()
    #     page = paginator.paginate_queryset(hotel, request)
    #     serializer = HotelRoomSerializer(page, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)
    
    # def create(self, request, *args, **kwargs):
    #     user = request.user.id
    #     if user.user_type != constants.ADMIN:
    #         return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
    #     sz = HotelRoomSerializer(data=request.data)
    #     if sz.is_valid(raise_exception = True):
    #         sz.save()
    #         _room = HotelRoom.objects.get(id=sz.data.get('id'))
    #         images = request.FILES.getlist('file')
    #         for image in images:
    #             activity_image = RoomImage(hotel_room=_room, image=image)
    #             activity_image.save()
    #     return Response(sz.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk, *args, **kwargs):
    #     user = request.user.id
    #     sz = HotelRoomSerializer(data=request.data)
    #     if user.user_type != constants.ADMIN:
    #         return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
    #     if sz.is_valid(raise_exception = True):
    #         _room = HotelRoom.objects.filter(id=pk).first()
    #         if not _room:
    #             return Response("ROOM_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
    #         _room.room_code = sz.data.get('room_code')
    #         _room.name = sz.data.get('name')
    #         _room.description = sz.data.get('description')
    #         _room.name = sz.data.get('offer')
    #         _room.price = sz.data.get('price')
    #         _room.save()
    #         return Response("UPDATE_ROOM_SUCCESS", status=status.HTTP_200_OK)

    # def destroy(self, request, pk, *args, **kwargs):
    #     user = request.user.id
    #     if user.user_type != constants.ADMIN:
    #         return Response("NOT_PERMISSION", status=status.HTTP_401_UNAUTHORIZED)
    #     _room = HotelRoom.objects.filter(id=pk).first()
    #     if not _room:
    #         return Response("ROOM_NOT_EXIST", status=status.HTTP_400_BAD_REQUEST)
    #     _room.delete()
    #     return Response("DELETE_ROOM_SUCCESS", status=status.HTTP_204_NO_CONTENT)