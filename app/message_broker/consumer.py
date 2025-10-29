import json
import asyncio
from app.message_broker.config import async_connection
from fastapi_mail import FastMail, MessageSchema
from app.schemas.email_config import conf

async def send_email(data):
    fm = FastMail(conf)

    email_msg = MessageSchema(
        subject=data['subject'],
        recipients=data['to'],
        body=data['body'],
        subtype='html'
    )

    try:
        await fm.send_message(email_msg)
        print(email_msg)
    except Exception as e:
        print(f'Error: {e}')

async def callback(msg: json):
    data = json.loads(msg.body.decode())

    await msg.ack()

    asyncio.create_task(send_email(data))

async def consumer_main():
    connection = await async_connection()
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            name='mini_blog',
            type='direct',
            durable=True
        )

        queue_names = ['likes', 'comments']

        for queue_name in queue_names:
            queue = await channel.declare_queue(name=queue_name, durable=True)

            await queue.bind(exchange, routing_key=queue_name)

            await queue.consume(callback)

            print(f"👂 Listening on queue: {queue_name}")

        await asyncio.Future()


    return {'msg': 'the notification was sent successfully'}

async def consumer_login():
    connection = await async_connection()
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(
            name='mini_blog_login',
            type='direct',
            durable=True
        )

        queue_name = 'ver_codes'

        queue = await channel.declare_queue(name=queue_name, durable=True)

        await queue.bind(exchange, routing_key=queue_name)

        await queue.consume(callback)

        print(f"👂 Listening on queue: {queue_name}")

        await asyncio.Future()


    return {'msg': 'the notification was sent successfully'}

if __name__ == '__main__':
    asyncio.run(consumer_main())


