from app.message_broker.config import async_connection
from aio_pika import Message
import json


async def publish_email(
        exchange_name: str,
        queue_name: str,
        to_email: str,
        subject: str,
        body: str
):
    connection = await async_connection()
    async with connection:
        async with connection.channel() as channel:

            exchange = await channel.declare_exchange(
                name=exchange_name,
                type='direct',
                durable=True
            )

            queue = await channel.declare_queue(
                name=queue_name,
                durable=True,
            )

            await queue.bind(exchange, routing_key=queue_name)

            event = {
                'to':[to_email],
                'subject':subject,
                'body':body,
            }

            message = Message(body=json.dumps(event).encode())

            await exchange.publish(message, routing_key = queue_name)


    return {'msg': 'the notification was sent successfully'}

