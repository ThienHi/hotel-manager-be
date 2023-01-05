import logging
from core import constants
from typing import Dict, List
from celery import shared_task
from django.db import connection
from pydantic import parse_obj_as
from django.utils import timezone
from core.schema import NatsChatMessage, MessageChat, ChatOptional
# from sop_chat_service.app_connect.models import Message, Attachment, ServiceSurvey, Room
# from sop_chat_service.zalo.utils.chat_support.format_message_zalo import format_attachment_type_from_zalo_message

logger = logging.getLogger(__name__)

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
