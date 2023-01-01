# -*- coding: utf-8 -*-
from typing import List, Optional, Dict
from pydantic import BaseModel
import ujson
import constants


class CustomBaseModel(BaseModel):

    class Config:
        json_loads = ujson.loads
        json_dumps = ujson.dumps
        fields = {
            'from_': 'from'
        }

    def dict(self, *args, **kwargs):
        kwargs.update({'by_alias': True})
        return super().dict(*args, **kwargs)


class NatsChatMessageAttachment(CustomBaseModel):
    type: Optional[str]
    payloadUrl: Optional[str]
    name: Optional[str]
    size: Optional[int]


class ChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}


class NatsChatMessage(CustomBaseModel):
    senderId: str
    recipientId: str
    timestamp: int
    text: Optional[str]
    mid: Optional[str]
    appId: str
    attachments: List[NatsChatMessageAttachment] = []
    typeChat: str
    typeMessage: Optional[str] = constants.NATS_MSG_TYPE_TEXT
    optionals: List[ChatOptional] = []
    room_id: Optional[str]


class Sender(CustomBaseModel):
    id: str


class Recipient(CustomBaseModel):
    id: str


class PayloadAttachment(CustomBaseModel):
    url: Optional[str]
    sticker_id: Optional[str]


class Attachment(CustomBaseModel):
    type: str
    payload: PayloadAttachment


class Message(CustomBaseModel):
    mid: str
    text: Optional[str]
    attachments: List[Attachment] = []


class Read(CustomBaseModel):
    watermark: int


class Messaging(CustomBaseModel):
    sender: Sender
    recipient: Recipient
    timestamp: int
    message: Optional[Message]
    read: Optional[Read]