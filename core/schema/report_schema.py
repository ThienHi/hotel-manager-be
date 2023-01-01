# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import List, Optional, Dict
from .base_model import CustomBaseModel
from core import constants


class DataReportWorker(CustomBaseModel):
    page_id: int
    page_name: str = ""
    room_id: str
    report_timestamp: Optional[int]
    uuid: Optional[str]
    type_chat : Optional[str] = constants.FACEBOOK
    user_id: List[str] = []
    is_new_chat: Optional[bool] = False
    is_new_conversation: Optional[bool] = False
    is_new_complete_conversation: Optional[bool] = False
    type_event: Optional[str] = constants.REPORT_ROUTER


class DataReportWS(CustomBaseModel):
    id: str
    name: str
    page_id: Optional[str] = None
    page_url: Optional[str] = None
    avatar_url: Optional[str] =None
    is_active : Optional[bool] = False
    is_deleted:Optional[bool] =False
    created_by:Optional[str] =None
    created_at:Optional[str] =None
    last_subscribe: Optional[str] =None
    type : Optional[str] = constants.FACEBOOK
    conversation_count: Optional[int] = 0
    followers_count: Optional[int] = 0
    likes_count: Optional[int] = 0
    user_id: List[str] = []
    event : Optional[str] = constants.NEW_REPORT_DATA


class ReportConversation(CustomBaseModel):
    page_id: int
    page_name: str = ""
    type: int
    numbers_conversation: int = 0
    complete_conversation: int
    timestamp: int
    created_at: str


class ReportFeedbackConversation(CustomBaseModel):
    page_id: int
    page_name: str = ""
    type: int
    feedback_rate: int = 0
    feedback_time: float
    timestamp: int
    created_at: str


class ReportSaleManByHour(CustomBaseModel):
    page_id: int
    page_name: str = ""
    type: str
    feedback_rate: int = 0
    feedback_time: float
    numbers_conversation: int = 0
    complete_conversation: int
    timestamp: int
    created_at: str
