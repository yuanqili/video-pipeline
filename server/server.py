import asyncio
import datetime
import websockets


async def image_recv_handler(websocket, path):
    counter = 0
    while True:
        counter += 1
        message = await websocket.recv()  # The websocket call to receive image
        await image_write(message, counter)


async def image_write(message, counter):
    print(f'[{datetime.datetime.now()}] received message')
    with open(f'image-recv-{counter}.jpg', 'wb') as f:
        f.write(message)


if __name__ == '__main__':
    # Creates a websocket waitable to receive images
    edge_conn = websockets.serve(image_recv_handler, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(edge_conn)
    asyncio.get_event_loop().run_forever()
