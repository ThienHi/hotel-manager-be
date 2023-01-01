# from .base import BaseWebSocketHandler
from core import constants
from core.utils import format_room_info
from core.handlers import BaseHandler
import logging
from sop_chat_service.app_connect.models import Message


logger = logging.getLogger(__name__)

class SendRoomWebSocketHandler(BaseHandler):
    send_message_type: str = constants.SEND_ROOM_INFO_WEBSOCKET

    async def handle_message(self, room,*args, **kwargs):
        room_info = await format_room_info(room)
        new_topic_publish = f'{constants.CORECHAT_TO_WEBSOCKET_NEW_ROOM}.{room.room_id}'
        await self.manager.nats_client.publish(new_topic_publish, room_info.json().encode())
        logger.debug(f"{new_topic_publish} ------{room_info} ")
