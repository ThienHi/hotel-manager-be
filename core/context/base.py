from core.abstractions import AbsAppContext
from typing import Dict
from core.abstractions import (
    AbsRouter,
    AbsManager
)
from core.routers import MessageTextRouter, MessageEmojiRouter, SendMessageRouter
from core.schema import NatsChatMessage, FormatSendMessage
from core.managers import StorageManager, WebSocketManager, SendMessageManager


# ----------------------------      BASE CONTEXT        ----------------------------
class BaseAppContext(AbsAppContext):
    _routers: Dict[str, AbsRouter] = {}
    _managers: Dict[str, AbsManager] = {}

# ----------------    RECEIVER    ----------------
    async def _get_routers(self, msg_type: str) -> Dict[str, AbsRouter]:
        for router_class in (MessageTextRouter, MessageEmojiRouter, SendMessageRouter, ):
            router_instance = router_class()
            self._routers.update({router_instance.msg_type: router_instance})
        return self._routers.get(msg_type)

    async def run_receiver(self, data: NatsChatMessage, **kwargs):
        router: AbsRouter = await self._get_routers(data.typeMessage)
        if router:
            router.bind_context(self)
            await router.process_message(data)
        else:
            print(f'not found router for {data.typeMessage}')


# ----------------    SEND MESSAGE    ----------------
    async def run_send_message(self, message: FormatSendMessage, **kwargs):
        router: AbsRouter = await self._get_routers(message.msg_status)
        if router:
            router.bind_context(self)
            await router.process_message(message)
        else:
            print(f'not found router for {message}')
    
    async def run_send_message_manager(self,manager_type: str, message: FormatSendMessage, **kwargs):
        manager: AbsManager = await self._get_manager(manager_type)
        if manager:
            manager.bind_context(self)
            await manager.initialize()
            await manager.process_message(message)
        else:
            print(f'not found router for {manager_type}')

# ----------------    MANAGER    ----------------
    async def _get_manager(self, manager_type: str) -> Dict[str, AbsManager]:
        # for manager_class in (StorageManager, WebSocketManager, SendMessageManager):
        for manager_class in (StorageManager, SendMessageManager):
            manager_instance = manager_class()
            self._managers.update({manager_instance.manager_type: manager_instance})
        return self._managers.get(manager_type)

    async def run_manager(self,room , manager_type: str, data: NatsChatMessage, **kwargs):
        manager: AbsManager = await self._get_manager(manager_type)
        if manager:
            manager.bind_context(self)
            await manager.initialize()
            await manager.process_message(room, data)
        else:
            print(f'not found router for {manager_type}')
# ----------------    END MANAGER    ----------------

# ----------------------------      END BASE CONTEXT        ----------------------------