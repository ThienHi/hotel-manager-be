# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List, Optional
import ujson


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


class ValueFrom(CustomBaseModel):
    id: str
    name: str


class ChangeValue(CustomBaseModel):
    from_: Optional[ValueFrom]
    link: Optional[str]
    post_id: Optional[str]
    created_time: Optional[int]
    item: str
    photo_id: Optional[str]
    published: Optional[int]
    verb: str


class Change(CustomBaseModel):
    value: ChangeValue
    field: str

# End change -------------------------------------------


class MessageEntry(CustomBaseModel):
    id: str
    time: int
    messaging: List[Messaging] = []
    changes: List[Change] = []


class FacebookIncomingMessage(CustomBaseModel):
    object: str
    entry: List[MessageEntry]
