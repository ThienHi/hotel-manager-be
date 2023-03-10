# from .base import BaseWebSocketHandler
from core import constants
from core.schema import NatsChatMessage
from core.handlers import BaseHandler
import logging
from core.utils import format_receive_message_to_websocket


logger = logging.getLogger(__name__)

class FacebookWebSocketHandler(BaseHandler):
    ws_type: str = constants.FACEBOOK

    async def handle_message(self, room, data: NatsChatMessage, *args, **kwargs):
        message_ws = format_receive_message_to_websocket(room, data, constants.SIO_EVENT_NEW_MSG_CUSTOMER_TO_SALEMAN)
        data_ws = message_ws.json().encode()
        # await self.manager.nats_client.publish_message_from_corechat_to_websocket_facebook(room_id = room.room_id, payload = data_ws)
        logger.debug(f"FacebookWebSocketHandler------ {data.uuid}")
