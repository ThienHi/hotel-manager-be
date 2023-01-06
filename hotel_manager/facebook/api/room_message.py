import logging
from django.db.models import Q
from rest_framework.decorators import action
from rest_framework import viewsets, permissions
from hotel_manager.utils.response import custom_response
from .serializers import (
    InfoSerializer,
    RoomMessageSerializer,
    RoomInfoSerializer,
    RoomSerializer,
    MessageSerializer
)
from hotel_manager.users.models import Room, Message

logger = logging.getLogger(__name__)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomSerializer
    queryset = Room.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def create(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    @action(detail=False, methods=["POST"], url_path="room-info")
    def room_info(self, request, *args, **kwargs):
        sz = RoomInfoSerializer(data=request.data, many=False)
        room = sz.validate(request, request.data)
        sz = InfoSerializer(room, many=False)
        return custom_response(200, "success", sz.data)

    @action(detail=False, methods=["POST"], url_path="list-room")
    def list_room(self, request, *args, **kwargs):
        user_header = request.user.id
        qs = Room.objects.filter((Q(user_id=user_header) | Q(admin_room_id=user_header))).distinct().order_by('-id')
        sz = RoomMessageSerializer(qs, context={'user_header': user_header}, many=True)
        return custom_response(200, "success", sz.data)

    def retrieve(self, request, pk=None):
        user_header = request.user.id
        room = Room.objects.filter((Q(user_id=user_header) | Q(admin_room_id=user_header)), room_id=pk).first()
        if not room:
            return custom_response(400, "Invalid room", [])
        message = Message.objects.filter(room_id=room).order_by("created_at")
        sz = MessageSerializer(message, many=True)
        data = {
            'room_id': room.room_id,
            'message': sz.data
        }
        return custom_response(200, "Get Message Successfully", data)
