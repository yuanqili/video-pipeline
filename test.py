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
        message = await producer()
        await websocket.send(message)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(producer_handler(websocket, path))
    done, pending = await asyncio.wait([consumer_task, producer_task],
                                       return_when=asyncio.FIRST_COMPLETED)
    for task in pending:
        task.cancel()


async def readMessage():
    async with websockets.connect('ws://localhost:4567') as websocket:
        message = await websocket.recv()
        await consumer(message)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(readMessage())
