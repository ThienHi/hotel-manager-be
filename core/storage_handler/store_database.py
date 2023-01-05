import logging
from core import constants
from core.handlers import BaseHandler
from core.schema.message_receive import NatsChatMessage
# from core.celery import celery_facebook_save_message_store_database
from core.utils import facebook_save_message_store_databases, format_receive_message
from django.utils import timezone

logger = logging.getLogger(__name__)


class StorageDataBase(BaseHandler):
    storage_type = constants.STORAGE_DATABASE

    async def handle_message(self, room, data: NatsChatMessage, *args, **kwargs):
        message_storage = format_receive_message(room, data)
        if data.typeChat == constants.FACEBOOK:
            await facebook_save_message_store_databases(room, message_storage)
            # celery_facebook_save_message_store_database.delay(room.id, data.dict())
            room.last_message_date = timezone.now()
