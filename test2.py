import asyncio

import websockets


async def consumer_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await consumer(message)


async def consumer(message):
    print(message)


async def producer_handler(websocket, path):
    while True:
        # message = await producer()
        # await websocket.send(message)
        await websocket.send("hello world")


async def producer():
    ...


async def handler(websocket, path=None):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


# async def send_message():
#     async with websockets.connect('ws://localhost:4567/q') as websocket:
#         websocket.send('good good study')


if __name__ == '__main__':
    ws = websockets.connect('ws://localhost:12313/q')
    asyncio.get_event_loop().run_until_complete(handler(ws))
    asyncio.get_event_loop().run_forever()
