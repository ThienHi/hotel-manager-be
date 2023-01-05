import requests
from core import constants
from django.utils import timezone
from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.conf import settings
from hotel_manager.users.models import FanPage, Message, Room
from hotel_manager.facebook.serializers.page_serializers import (
    FanPageSerializer,
    FacebookAuthenticationSerializer,
    FacebookConnectPageSerializer,
    DeleteFanPageSerializer,
)
from hotel_manager.facebook.serializers.message_facebook_serializers import MessageFacebookSerializer
from hotel_manager.utils.response import custom_response
from .chat_message import handle_incoming_chat_message
from rest_framework.views import APIView
import asyncio, json, uuid
from core.utils import (
    api_send_message_file_facebook,
    get_message_from_mid,
    facebook_format_data_from_mid_facebook,
    api_send_message_text_facebook
)
from core.context import AppContextManager
from core.schema import FormatSendMessage
from core import constants
from pydantic import parse_raw_as


class FacebookWebhookView(APIView):
    permission_classes = (permissions.AllowAny,)
    # serializer_class = WebhookFacebookSerializer

    def post(self, request,*args, **kwargs):
        body = request.data
        print(type(body), "post request --------------------------------------- ", body)
        asyncio.run(handle_incoming_chat_message(json.dumps(body).encode('utf-8')))
        return Response(status=status.HTTP_200_OK)

    def get(self, request, format=None, *args, **kwargs):
        hub_mode = request.GET.get('hub.mode')
        hub_challenge = request.query_params.get('hub.challenge')
        challenge = hub_challenge

        hub_verify_token = request.GET.get('hub.verify_token')
        print(f'hub_mode {hub_mode} - hub_challenge {hub_challenge} ---- {challenge} - hub_verify_token {hub_verify_token}')
        return Response(data=int(challenge), status=status.HTTP_200_OK)


class ReportMessageView(generics.ListAPIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request,*args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class FacebookViewSet(viewsets.ModelViewSet):
    queryset = FanPage.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = FacebookAuthenticationSerializer

    def list(self, request, *args, **kwargs):
        user_header = request.user.id
        pages = FanPage.objects.filter(user_id=user_header, type=constants.FACEBOOK,is_deleted= False)
        sz = FanPageSerializer(pages, many=True)
        return custom_response(200, "Get list page successfully", sz.data)

    @action(detail=False, methods=["POST"], url_path="list-page")
    def get_page(self, request, *args):
        user_header = request.user.id
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        graph_api = settings.FACEBOOK_GRAPH_API
        # try:
        query = {'redirect_uri': sz.data['redirect_url'], 'code': sz.data['code'],
                    'client_id': settings.FACEBOOK_APP_ID, 'client_secret': settings.FACEBOOK_APP_SECRET}
        access_response = requests.get(f'{graph_api}/oauth/access_token', params=query)
        if access_response.status_code == 200:
            page_query = {'access_token': access_response.json()['access_token']}
            me = requests.get(f'{graph_api}/me', params=page_query)
            fb_user_id= me.json()['id']
            page_response = requests.get(f'{graph_api}/me/accounts', params=page_query)
            if page_response.status_code == 200:
                data = page_response.json()
                id = []
                if  not data['data']:
                    pages = FanPage.objects.filter(type='facebook',user_id=user_header,fanpage_user_id=fb_user_id)
                    for remove_page in pages:
                        remove_page.access_token_page=None
                        remove_page.is_active=False
                        remove_page.save()
                    return custom_response(400, "List Page Is Null", [])
                else:
                    for item in data['data']:
                        page = FanPage.objects.filter(type='facebook',page_id=item['id'],user_id=user_header,fanpage_user_id=fb_user_id).first()
                        id.append(item['id'])
                        avt_id = item['id']
                        page_url_query = {
                            'access_token': access_response.json()['access_token'],
                            'fields': settings.URL_FIELD
                        }
                        page_url_res = requests.get(f'{graph_api}/{avt_id}', params=page_url_query)
                        page_json = page_url_res.json()
                        if page is None:
                            FanPage.objects.create(
                                page_id=item['id'], name=item['name'], access_token_page=item['access_token'],
                                avatar_url=f'{graph_api}/{avt_id}/picture',
                                user_id=user_header,fanpage_user_id=fb_user_id,
                                is_deleted=False,
                                page_url=page_json['link']
                            )
                        else:
                            page.access_token_page=item['access_token']
                            page.name=item['name']
                            page.avatar_url=f'{graph_api}/{avt_id}/picture'
                            page.is_deleted=False
                            page.page_url =page_json['link']
                            page.save()
                page_remove = FanPage.objects.filter(user_id=user_header,fanpage_user_id=fb_user_id,type='facebook').exclude(page_id__in=id )
                for item in page_remove:
                    item.is_active = False
                    item.is_deleted=True
                    item.access_token_page = ''
                    item.save()
                return custom_response(200, "Get list page success", [])
            else:
                return custom_response(500, "INTERNAL_SERVER_ERROR", [])
        else:
            return custom_response(500, "INTERNAL_SERVER_ERROR", [])

    @action(detail=False, methods=["POST"], url_path="page/subscribe")
    def subscribe_page(self, request, *args):
        user_header = request.user.id
        sz = FacebookConnectPageSerializer(data=request.data)
        if sz.is_valid(raise_exception=True):
            graph_api = settings.FACEBOOK_GRAPH_API
            if sz.data.get('is_subscribe') == True:
                page_id = sz.data.get('page_id')
                try:
                    page = FanPage.objects.filter(type=constants.FACEBOOK, page_id=page_id, user_id=user_header).first()
                    if page.is_active:
                        return custom_response(400, "Error: This Fanpage Have Been Subscribe!!!", [])
                    query_field = {'subscribed_fields': settings.SUBSCRIBE_FIELDS,
                                   'access_token': page.access_token_page}
                    response = requests.post(f'{graph_api}/{page_id}/subscribed_apps', data=query_field)
                    if response.status_code == 200:
                        data = response.json()
                        if data['success']:
                            if page:
                                if page.is_active:
                                    pass
                                page.is_active = True
                                page.last_subscribe = timezone.now()
                                page.save()
                            else:
                                pass
                        message = "Subscribed successfully"
                        sz = FanPageSerializer(page, many=False)
                        return custom_response(200, message, sz.data)
                    else:
                        return custom_response(500, "INTERNAL_SERVER_ERROR", [])
                except Exception:
                    return custom_response(500, 'INTERNAL_SERVER_ERROR', [])
            else:
                page_id = request.data.get('page_id')
                try:
                    page = FanPage.objects.filter(page_id=page_id, user_id=user_header).first()
                    if page:
                        if page.is_active:
                            page_id = page.page_id
                            query_field = {'access_token': page.access_token_page}
                            response = requests.delete(f'{graph_api}/{page_id}/subscribed_apps', data=query_field)
                            if response.status_code == 200:
                                data = response.json()
                                if data['success']:
                                    page.is_active = False
                                    page.last_subscribe = timezone.now()
                                    # page.access_token_page = "invalid"
                                    page.save()
                                else:
                                    pass
                                message = "Subscribed successfully"
                                sz = FanPageSerializer(page, many=False)
                                return custom_response(200, message, sz.data)
                            else:
                                message = response.json().get('error').get('message')
                                return custom_response(500, "INTERNAL_SERVER_ERROR", [])
                        else:
                            page_id = page.page_id
                            query_field = {'access_token': page.access_token_page}
                            response = requests.delete(f'{graph_api}/{page_id}/subscribed_apps', data=query_field)
                            if response.status_code == 200:
                                data = response.json()
                            else:
                                message = response.json().get('error').get('message')
                                return custom_response(500, "INTERNAL_SERVER_ERROR", [])
                    else:
                        pass
                except Exception as e:
                    return custom_response(500, 'INTERNAL_SERVER_ERROR', [])

    @action(detail=False, methods=['POST'], url_path='delete')
    def delete(self, request, *args, **kwargs):
        user_header = request.user.id
        sz = DeleteFanPageSerializer(data = request.data)
        sz.is_valid(raise_exception=True)
        graph_api = settings.FACEBOOK_GRAPH_API
        for id in sz.data['id']:
            page = FanPage.objects.filter(id=id, user_id=user_header).first()
            page_id = page.id
            if page.is_active == True:
                query_field = {'access_token': page.access_token_page}
                response = requests.delete(f'{graph_api}/{page_id}/subscribed_apps', data=query_field)
                if response.status_code == 200:
                    data = response.json()
                    if data['success']:
                        page.is_deleted= True
                        page.is_active = False
                        page.access_token_page = "invalid"
                    else:
                        pass
                else:
                    page.is_deleted= True
                    page.is_active = False
                    page.access_token_page = "invalid"
            else :
                page.is_deleted= True
                page.is_active = False
                page.access_token_page = "invalid"
            page.save() 
        return custom_response(200,'Delete Pages Successfully',[])

    def destroy(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def create(self, request):
        pass

app_context = AppContextManager()

async def send_message_fb(msg):
    _message = parse_raw_as(FormatSendMessage, msg)
    await app_context.run_send_message(_message)

class MessageFacebookViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = MessageFacebookSerializer

    @action(detail=False, methods=["POST"], url_path="send")
    def send_message(self, request, *args, **kwargs):
        serializer = MessageFacebookSerializer(data=request.data)
        room, data, message_type_attachment,user_header = serializer.validate(request ,request.data)
        # send message
        if room.page_id.is_active:
            if message_type_attachment:
                for file in data['files']:
                    res = api_send_message_file_facebook(room.page_id.access_token_page, data, file)
                    if not res:
                        return custom_response(400, "error", "Send message to Facebook error")
                    message_response = get_message_from_mid(room.page_id.access_token_page, res['message_id'])
                    _uuid = uuid.uuid4()
                    data_mid_json = facebook_format_data_from_mid_facebook(room, message_response, _uuid,user_header)
                    asyncio.run(send_message_fb(json.dumps(data_mid_json).encode()))
                return custom_response(200, "success", "Send message to Facebook success")
            else:
            # get message from mid
                res = api_send_message_text_facebook(room.page_id.access_token_page, data)
                if not res:
                    return custom_response(400, "error", "Send message to Facebook error")
                message_response = get_message_from_mid(room.page_id.access_token_page, res['message_id'])
                _uuid = uuid.uuid4()
                data_mid_json = facebook_format_data_from_mid_facebook(room, message_response, _uuid,user_header)
                asyncio.run(send_message_fb(json.dumps(data_mid_json).encode()))
                room.last_message_date = timezone.now()
                return custom_response(200, "success", "Send message to Facebook success")
        else:
            return custom_response(400, "Send message failed", "Send message to Facebook failed")
