from rest_framework import serializers
from hotel_manager.users.models import Attachment, Message, FanPage, Room, UserApp
from django.db.models import Q
import re


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'mid', 'type', 'url', 'name', 'size']


class GetMessageSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField(source='get_attachments', read_only=True)

    class Meta:
        model = Message
        fields = ['attachments', 'sender_id', 'recipient_id', 'text', 'reply_id', 'is_sender', 'created_at', 'uuid']

    def get_attachments(self, obj):
        attachments = Attachment.objects.filter(mid=obj.id)
        sz = AttachmentSerializer(attachments, many=True)
        return sz.data if attachments else None


class RoomSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(source='get_last_message', read_only=True)
    unseen_message_count = serializers.SerializerMethodField(source='get_unseen_message_count', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'user_id', 'name', 'type', 'note', 'approved_date', 'status',
                  'completed_date', 'conversation_id', 'created_at', 'last_message', 'room_id', "unseen_message_count"]

    def get_unseen_message_count(self, obj):
        count = Message.objects.filter(room_id=obj, is_sender=False, is_seen__isnull=True).count()
        return count

    def get_last_message(self, obj):
        message = Message.objects.filter(room_id=obj).order_by('-id').first()
        sz = GetMessageSerializer(message)
        return sz.data


class RoomInfoSerializer(serializers.Serializer):
    room_id = serializers.CharField(required=False)

    def validate(self, request, attrs):
        user_header = request.user.id
        room = Room.objects.filter((Q(user_id=user_header) | Q(admin_room_id=user_header)),
                                   room_id=attrs.get("room_id")).first()
        if not room:
            raise serializers.ValidationError({"room": "Room Invalid"})
        return room


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserApp
        fields = "__all__"


class InfoSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(source='get_last_message', read_only=True)
    user_info = serializers.SerializerMethodField(source='get_user_info', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'user_id', 'name', 'type', 'note', 'approved_date', 'status',
                  'completed_date', 'conversation_id', 'created_at', 'last_message', 'room_id', 'user_info']

    def get_last_message(self, obj):
        if obj.type.lower() == "facebook":
            message = Message.objects.filter(room_id=obj, is_sender=False).order_by('-id').first()
            sz = GetMessageSerializer(message)
            return sz.data
        else:
            message = Message.objects.filter(room_id=obj).order_by('-id').first()
            sz = GetMessageSerializer(message)
            return sz.data

    def get_user_info(self, obj):
        user_info = UserApp.objects.filter(external_id=obj.external_id).first()
        sz_user_info = UserInfoSerializer(user_info)
        return sz_user_info.data


class RoomMessageSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField(source='get_last_message', read_only=True)
    user_info = serializers.SerializerMethodField(source='get_user_info', read_only=True)

    class Meta:
        model = Room
        fields = ['id', 'user_id', 'name', 'type', 'approved_date', 'status', 'external_id',
                  'completed_date', 'last_message', 'room_id', 'user_info']

    def get_last_message(self, obj):
        message = Message.objects.filter(room_id=obj).order_by('-id').first()
        sz = GetMessageSerializer(message)
        return sz.data

    def get_user_info(self, obj):
        user_info = UserApp.objects.filter(external_id=obj.external_id).first()
        sz_user_info = UserInfoSerializer(user_info)
        return sz_user_info.data



class MessageSerializer(serializers.ModelSerializer):
    class Meta: 
        model= Message
        fields = "__all__"
        