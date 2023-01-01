# -*- coding: utf-8 -*-
import logging
from core import constants
from schemas.chat_message_schema import FacebookIncomingMessage
from schemas.nats import NatsChatMessage, NatsChatMessageAttachment
from schemas.nats import Messaging as FacebookMessaging
from schemas.chat_message_schema import FacebookIncomingMessage
from hotel_manager.utils.nats_publish import connect_nats_client_publish_websocket

debug_logger = logging.getLogger(constants.DEBUG_LOGGER_NAME)


async def facebook_create_nats_chat_message(
    entry_id: str,
    messaging: FacebookMessaging,
    chat_type: str
) -> str:
    return NatsChatMessage(
        senderId=messaging.sender.id,
        recipientId=messaging.recipient.id,
        timestamp=messaging.timestamp,
        text=messaging.message.text,
        mid=messaging.message.mid,
        appId=entry_id,
        attachments=[
            NatsChatMessageAttachment(
                type=attachment.type,
                payloadUrl=attachment.payload.url
            ) for attachment in messaging.message.attachments
        ],
        typeChat=chat_type
    ).json()


async def facebook_publish_to_nats_each_page_id(incoming_message: FacebookIncomingMessage):
    # create data in right format then publish into nats
    results = []
    for entry in incoming_message.entry:
        for messaging in entry.messaging:
            if messaging.message and messaging.recipient and messaging.recipient.id:
                nats_subject = "WEBHOOK_TO_CORECHAT_MESSAGE"
                if entry.id and nats_subject:
                    nats_msg = await facebook_create_nats_chat_message(entry.id, messaging, 'facebook')

                    _res = await connect_nats_client_publish_websocket(
                        nats_subject,
                        nats_msg.encode()
                    )
                    results.append({'subject': nats_subject, 'res': _res})
    return results


async def handle_incoming_chat_message(request_body: bytes):
    try:
        incoming_message = FacebookIncomingMessage.parse_raw(request_body)
    except Exception as e:
        debug_logger.exception(f'facebook parse FacebookIncomingMessage get exception {e}')
        return

    res = await facebook_publish_to_nats_each_page_id(incoming_message)
    debug_logger.info(f'facebook publish nats results {res=}')
