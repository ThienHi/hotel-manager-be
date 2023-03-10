from typing import Dict
from core.schema import NatsChatMessage
from core.abstractions import SingletonClass, AbsAppContext, AbsHandler, AbsManager
from core.stream import NatsClient
from core.stream.redis_connection import redis_client


class BaseManager(SingletonClass, AbsManager):
    manager_type: str = None
    _handlers: Dict[str, AbsHandler] = {}

    async def initialize(self, *args, **kwargs):
        if self._initialized:
            return
        self._handlers = await self._get_handlers()
        self._initialized = True
        # await self.nats_client.connect()

    def _singleton_init(self, **kwargs):
        self._initialized: bool = False
        self._is_connected: bool = False
        self._handlers: Dict[str, AbsHandler] = {}
        # self.nats_client = NatsClient()
        self.redis_client = redis_client

    def bind_context(self, context: AbsAppContext, **kwargs):
        self.context = context
    
    # ----------------    HANDLER    ----------------
    async def _get_handlers(self) -> Dict[str, AbsHandler]:
        pass

    async def process_message(self, data: NatsChatMessage, *args, **kwargs):
        handler: AbsHandler = self._handlers.get(data.typeChat)
        if handler:
            await handler.set_manager(self)
            await handler.handle_message(data, **kwargs)
        else:
            print(f'{self.__class__.__name__} not found handler for {data}')