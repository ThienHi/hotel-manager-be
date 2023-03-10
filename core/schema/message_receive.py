# -*- coding: utf-8 -*-
from typing import List, Optional, Dict
from .base_model import CustomBaseModel
from core import constants


class NatsChatMessageAttachment(CustomBaseModel):
    name:Optional[str]
    type: Optional[str]
    payloadUrl: Optional[str]
    size: Optional[str]

class NatsChatMessageUserInfo(CustomBaseModel):
    title: Optional[str]
    value: Optional[str]
class ChatOptional(CustomBaseModel):
    chat_type: str
    data: Optional[Dict] = {}

class LogMessageSchema(CustomBaseModel):
    log_type:Optional[str]
    message: Optional[str]
    room_id: Optional[str]
    from_user: Optional[str]
    to_user: Optional[str]
    created_at: Optional[str]

class NatsChatMessage(CustomBaseModel):
    senderId: Optional[str]
    recipientId: Optional[str]
    timestamp: int
    text: Optional[str]
    mid: Optional[str]
    appId: str
    attachments: List[NatsChatMessageAttachment] = []
    user_info: List[NatsChatMessageUserInfo] = []
    typeChat: str
    typeMessage: Optional[str] = constants.MESSAGE_TEXT
    optionals: List[ChatOptional] = []
    uuid: Optional[str] = ""
    room_id: Optional[str] = None
    log_message: Optional[LogMessageSchema] = None
    is_new_room: Optional[bool] = False
    is_new_chat: Optional[bool] = False
    is_new_conversation: Optional[bool] = False
    is_new_complete_conversation: Optional[bool] = False
