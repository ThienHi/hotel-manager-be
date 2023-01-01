from sop_chat_service.app_connect.models import Message, Attachment
from core.utils.api_facebook_app import get_message_from_mid
from core.utils.format_message_for_websocket import facebook_format_mid
from django.utils import timezone
from core.schema import MessageChat
from core.schema import NatsChatMessage
from core.schema import FormatSendMessage
from core import constants
from django.db import connection
import logging

logger = logging.getLogger(__name__)

async def facebook_save_message_store_databases(room, msg: MessageChat):
    data_res = get_message_from_mid(room.page_id.access_token_page, msg.mid)
    data = facebook_format_mid(room, data_res)
    message = Message(
        room_id = room,
        fb_message_id = data.get("mid"),
        sender_id = data.get("sender_id"),
        recipient_id = data.get("recipient_id"),
        text = data.get("text"),
        uuid = msg.uuid
    )
    message.save()
    if data.get("attachments"):
        for attachment in data.get("attachments"):
            Attachment.objects.create(
                mid = message,
                type = attachment.get('type'),
                attachment_id = attachment.get('id'),
                url = attachment.get('url') if attachment.get('url') else attachment.get('video_url'),
                name = attachment.get('name'),
                size = attachment.get('size')
            )
    return


async def facebook_save_message_store_database(room, msg: NatsChatMessage):
    try:
        cursor = connection.cursor()
        cursor.execute(constants.INSERT_MESSAGE_ROOM, (msg.uuid, msg.mid, msg.senderId, msg.recipientId, None, None, None,
            msg.text, None, None, False, None, timezone.now(), msg.timestamp, room.id))
        message = Message.objects.order_by('-id').filter(fb_message_id=msg.mid, room_id=room.id).first()
        if msg.attachments:
            for attachment in msg.attachments:
                cursor.execute(constants.INSERT_ATTACHMENT, (None, None, attachment.type, attachment.payloadUrl, attachment.name, attachment.size, message.id))
        return
    except Exception as e:
        logger.error(f'EXCEPTION Facebook storage message as: {e}')


async def facebook_send_message_store_database(room, _message: FormatSendMessage):
    message = Message(
        room_id = room,
        fb_message_id = _message.mid,
        sender_id = _message.sender_id,
        recipient_id = _message.recipient_id,
        text = _message.text,
        is_sender= True,
        is_seen = timezone.now(),
        uuid = _message.uuid
    )
    message.save()
    attachments = _message.attachments
    if attachments:
        for attachment in attachments:
            Attachment.objects.create(
                mid = message,
                type = attachment.type,
                attachment_id = attachment.id,
                url = attachment.url if attachment.url else attachment.video_url,
                name = attachment.name,
                size = attachment.size
            )
    return
