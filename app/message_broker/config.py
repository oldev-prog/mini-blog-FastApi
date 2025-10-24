import pika
import aio_pika
from pika import ConnectionParameters

MQ_HOST = '0.0.0.0'
MQ_PORT = 5672
MQ_USER = 'guest'
MQ_PASSWORD = 'guest'

sync_connection_params = pika.ConnectionParameters(
            host=MQ_HOST,
            port=MQ_PORT,
            credentials=pika.PlainCredentials(MQ_USER, MQ_PASSWORD)
                          )

async def async_connection():
    async_connection_params = await aio_pika.connect_robust(host=MQ_HOST, port=MQ_PORT,)
    return async_connection_params



