import requests
import logging
import time
import asyncio, ujson
from django.conf import settings
from celery import shared_task
from core import constants
from core.stream.redis_connection import redis_client
from core.utils.nats_connect import publish_data_to_nats
from core.utils.format_message_for_websocket import format_room
from typing import Dict
# from sop_chat_service.app_connect.models import Room, UserApp,FanpageReport
# from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)


@shared_task(name = constants.CELERY_TASK_ASSIGN_CHAT)
def celery_task_assign_chat(_data: Dict, *args, **kwargs):
    try:
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-User-Id': _data.get('X-Auth-User-Id')
        }
        url = settings.CUSTOMER_SERVICE_URL + settings.API_ASSIGN_CHAT
        response = requests.post(url=url, headers=headers, data=ujson.dumps(_data))
        return response.text
    except Exception as e:
        return f"Exception Verify information ERROR: {e}"



@shared_task(name = constants.COLLECT_LIVECHAT_SOCIAL_PROFILE)
def collect_livechat_social_profile(*args, **kwargs):
    room_id = kwargs.get('room_id')
    try:
        payload = {
            'type': constants.FCHAT,
            'page': kwargs.get('live_chat_id'),
            'ip': kwargs.get('client_ip'),
            'device': kwargs.get('client_info'),
            'browser': kwargs.get('client_info'),
            "room_id": kwargs.get('room_id'),
            'browser_origin': kwargs.get('browser_origin')
        }
        redis_client.set(f'{constants.COLLECT_LIVECHAT_SOCIAL_PROFILE}__{room_id}', ujson.dumps(payload))
        return payload
    except Exception as e:
        return f"Exception Verify information ERROR: {e}"


@shared_task(name = constants.UPDATE_PROFILE_USER_AFTER_FOLLOW_ZALO)
def update_profile(_room_id,_room_user_id,_user_app_name,_user_app_gender,*args, **kwargs):
    try:
        logger.debug(f'update_profile **************************************************************** ')
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-User-Id': _room_user_id
        }
        url = f'{settings.CUSTOMER_SERVICE_URL}{settings.API_UPDATE_INFORMATION}/{_room_id}'
        gender='Khác'
        if not _user_app_gender:
            pass
        elif _user_app_gender.lower() =="male" :
            gender = 'Nam'
        else:
            gender = 'Nữ'
        
        payload = {
            'name': _user_app_name,
            'gender': gender,
        }
        response = requests.put(url=url,data=ujson.dumps(payload) ,headers=headers )
        return response.text
    except Exception as e:
        return f"Exception Verify information ERROR: {e}"



@shared_task(name = constants.GET_CONTACT_FB_FAN_PAGE)
def update_contact_fb(page_id,page_access_token,report_id,*args, **kwargs):
    try:
        page_query = {
                          'access_token': page_access_token,
                          'fields': settings.FB_CONTACT_FILED
                          }
        page_res = requests.get(f'{settings.FACEBOOK_GRAPH_API}/{page_id}', params=page_query)
        page = page_res.json()
        report= FanpageReport.objects.get(id= report_id)
        report.followers_count= page['followers_count']
        report.likes_count = page['fan_count']
        report.save()
        return page_res.text
    except Exception as e:
        return f"Exception Get ERROR: {e}"

@shared_task(name = constants.GET_CONTACT_ZALO_FAN_PAGE)
def update_contact_zalo(page_access_token,report_id,*args, **kwargs):
    try:
        page_query = {
                          'data': settings.ZALO_CONTACT_FIELD
                          }
        headers={
            'access_token':page_access_token
        }
        page_res = requests.get(f'{settings.ZALO_OA_OPEN_API}/getfollowers', params=page_query,headers=headers)
        page = page_res.json()['data']
        report= FanpageReport.objects.get(id= report_id)
        report.followers_count= page['total']
        report.save()
        return page_res.text
    except Exception as e:
        return f"Exception Get ERROR: {e}"
