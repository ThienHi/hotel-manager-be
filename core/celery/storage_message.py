import logging
from core import constants
from typing import Dict, List
from celery import shared_task
from django.db import connection
from pydantic import parse_obj_as
from django.utils import timezone
from core.schema import NatsChatMessage, MessageChat, ChatOptional
from sop_chat_service.app_connect.models import Message, Attachment, ServiceSurvey, Room
from sop_chat_service.zalo.utils.chat_support.format_message_zalo import format_attachment_type_from_zalo_message

logger = logging.getLogger(__name__)


@shared_task(name = constants.CELERY_TASK_STORAGE_MESSAGE_LIVECHAT)
def live_chat_save_message_store_database(room: Dict, data: NatsChatMessage):
    logger.info(f'LiveChat storage message with data: {data}')
    is_sender = False
    if data.optionals:
        if data.optionals[0].data.get("is_sender"):
            is_sender = data.optionals[0].data.get("is_sender")
    _room = Room.objects.filter(id=room.get('id')).first()
    if _room.type == constants.LIVECHAT:
        message = Message(
            room_id = _room,
            fb_message_id = data.mid,
            sender_id = _room.user_id if is_sender else data.senderId,
            is_sender =is_sender,
            recipient_id = data.recipientId,
            text = data.text,
            uuid = data.uuid,
            timestamp = data.timestamp
        )
        message.save()
        if data.attachments:
            for attachment in data.attachments:
                Attachment.objects.create(
                    mid = message,
                    name = attachment.name,
                    size = attachment.size,
                    type = attachment.type,
                    url = attachment.payloadUrl,
                )
        if data.optionals:
            if data.optionals[0].data.get("user_info"):
                for item in data.optionals[0].data.get("user_info"):
                    ServiceSurvey.objects.create(
                        mid = message,
                        name = item['title'],
                        value = item['value']
                    )
        _room.last_message_date = timezone.now()
        return "LiveChat storage message success"


@shared_task(name = constants.CELERY_TASK_STORAGE_MESSAGE_FACEBOOK)
def celery_facebook_save_message_store_database(room_id, msg: Dict):
    parse_msg = parse_obj_as(NatsChatMessage, msg)
    try:
        cursor = connection.cursor()
        cursor.execute(constants.INSERT_MESSAGE_ROOM, (parse_msg.uuid, parse_msg.mid, parse_msg.senderId, parse_msg.recipientId, None, None, None,
            parse_msg.text, None, None, False, None, timezone.now(), parse_msg.timestamp, room_id))
        cursor.execute(constants.SELECT_MESSAGE, (room_id, parse_msg.mid))
        message = cursor.fetchall()[0]
        if msg['attachments']:
            for attachment in msg['attachments']:
                cursor.execute(constants.INSERT_ATTACHMENT, (None, None, attachment['type'], attachment['payloadUrl'], attachment['name'], attachment['size'], message[0]))
        return "Facebook storage message success"
    except Exception as e:
        logger.error(f'EXCEPTION Facebook storage message as: {e}')


@shared_task(name = constants.CELERY_TASK_STORAGE_MESSAGE_ZALO)
def celery_zalo_save_message_store_database(room_id: str, msg: Dict, data: Dict):
    parse_msg_chat = parse_obj_as(MessageChat, msg)
    parse_msg = parse_obj_as(NatsChatMessage, data)
    optionals = parse_msg.optionals
    try:
        cursor = connection.cursor()
        cursor.execute(constants.INSERT_MESSAGE_ROOM, (parse_msg_chat.uuid, parse_msg_chat.mid, parse_msg_chat.sender_id, parse_msg_chat.recipient_id, None, None, None,
            parse_msg_chat.text, None, None, False, None, timezone.now(), parse_msg_chat.timestamp, room_id))
        cursor.execute(constants.SELECT_MESSAGE, (room_id, parse_msg_chat.mid))
        message = cursor.fetchall()[0]
        if parse_msg_chat.attachments:
            for index, attachment in enumerate(parse_msg_chat.attachments):
                if optionals[index] and optionals[index].data.get('attachments'):
                    reformatted_attachment_type, attachment_name, attachment_size, attachment_id = format_attachment_type_from_zalo_message(attachment, optionals, index)
                cursor.execute(constants.INSERT_ATTACHMENT, (attachment_id, None, reformatted_attachment_type,
                    attachment.url, attachment_name, attachment_size, message[0]))
        return "Zalo storage message success"
    except Exception as e:
        logger.error(f'EXCEPTION Zalo storage message as: {e}')
