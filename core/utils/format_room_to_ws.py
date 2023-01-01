from core import constants
from sop_chat_service.app_connect.models import Room,UserApp,FanPage
from core.schema import RoomInfo,FanPageInfo,UserInfo

async def format_room_info(room:Room):
    user_id = []
    if room.admin_room_id:
        user_id = [room.admin_room_id, room.user_id]
    else:
        user_id = [room.user_id]
    user_info =[]
    fanpage_info=[]
    # if room.page_id:
        # fanpage_qs = FanPage.objects.filter(id=room.page_id.id).first()
        # if fanpage_qs:
    fanpage_info=FanPageInfo(
        name= room.page_id.name if room.page_id else "",
        avatar_url= room.page_id.avatar_url if room.page_id else ""
    )
    user_info_qs = UserApp.objects.filter(external_id=room.external_id).first()
    if user_info_qs:
        user_info =UserInfo(
            id= user_info_qs.id,
            external_id= user_info_qs.external_id,
            name= user_info_qs.name,
            email= user_info_qs.email,
            phone= user_info_qs.phone,
            avatar= user_info_qs.avatar,
            gender= user_info_qs.gender
        )
    room_info = RoomInfo(
        user_id = user_id,
        event =constants.NEW_ROOM_INFO,
        id = room.id,
        room_id= room.room_id ,
        type = room.type,
        name = room.name,
        approved_date = str(room.approved_date),
        assign_reminder = None,
        status  = room.status,
        created_at= str(room.created_at),
        completed_date = str(room.completed_date),
        conversation_id=room.conversation_id,
        unseen_message_count= 0,
        last_message=None,
        user_info=user_info,
        fanpage=fanpage_info,
        label= []
    )
    
    return room_info
