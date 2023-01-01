from .base import BaseAppContext
from core.abstractions import SingletonClass
from core.stream.redis_connection import redis_client
from core.stream import NatsClient


class AppContextManager(BaseAppContext, SingletonClass):

    async def initialize(self, *args, **kwargs):
        if self._initialized:
            return
        self._initialized = True
        await self.nats_client.connect()

    def _singleton_init(self, **kwargs):
        self._initialized: bool = False
        self._test = "Test AppContextManager"
        self.redis_client = redis_client
        self.nats_client = NatsClient()
