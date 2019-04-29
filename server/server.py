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
    filename, payload = decode_message(message)
    print(f'[{datetime.datetime.now()}] received image: {filename}')
    with open(filename, 'wb') as f:
        f.write(payload)


def decode_message(message):
    header_size = int.from_bytes(message[:2], byteorder='big')
    header = message[2:header_size+2].decode('utf-8')
    payload = message[header_size+2:]
    return header, payload


if __name__ == '__main__':
    # Creates a websocket waitable to receive images
    edge_conn = websockets.serve(image_recv_handler, 'localhost', 8765)
    asyncio.get_event_loop().run_until_complete(edge_conn)
    asyncio.get_event_loop().run_forever()
