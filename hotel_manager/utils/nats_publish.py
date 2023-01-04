import nats
from django.conf import settings

async def connect_nats_client_publish_websocket(new_topic_publish, data_mid):
    print(" settings.NATS_URL ========== ", settings.NATS_URL)
    nats_client = await nats.connect(settings.NATS_URL)
    await nats_client.publish(new_topic_publish, bytes(data_mid))
    await nats_client.close()
    return