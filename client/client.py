import asyncio
from urllib.parse import urlunparse

import cv2
import websockets
from tqdm import tqdm


def build_url(netloc, port, scheme='ws', path='', params='', query='', fragment=''):
    """
    Build a url using given arguments. Parameter names follow urllib convention.
    """
    return urlunparse((scheme, f'{netloc}:{port}', path, params, query, fragment))


async def framer(url, video_path, output_path, quality, processor):
    """
    Processes a video at `video_path` frame by frame, using `processor`, then
    sends processed frames via a websocket to the other side.

    Args:
        url: Server address, e.g., ws://localhost:8765 for a websocket connection.
        video_path: The video to be processed.
        output_path: Saved frames of the processed video.
        quality: At which quality level the frames are compressed, range 0–100.
            Higher the better.
        processor: A function of type (frame) -> frame. It receives a frame as
            input and returns a frame.
    """
    async with websockets.connect(url) as websocket:

        # Opens the video at `video_path`
        cap = cv2.VideoCapture(video_path)
        frame_count = int(cv2.VideoCapture.get(cap, int(cv2.CAP_PROP_FRAME_COUNT)))
        progress_bar = tqdm(total=frame_count, ncols=80)

        # Processes each frame
        for index in range(1, frame_count+1):
            ret, frame = cap.read()
            if not ret:
                break
            progress_bar.update()

            # Process the frame, using the given `processor`, writes to file
            processed_frame = processor(frame)
            filename = f'{output_path}/image-gen-{index}.jpg'
            cv2.imwrite(filename, processed_frame, [cv2.IMWRITE_JPEG_QUALITY, quality])

            # Sends the processed image to the server
            with open(filename, 'rb') as f:
                bits = f.read()
                await websocket.send(bits)

        # Closes
        progress_bar.close()
        cap.release()
        cv2.destroyAllWindows()


def grayscale(frame):
    """
    Transforms a image to grayscale.

    Args:
        frame: Input frame to be processed.

    Returns:
        Grayscaled frame.
    """
    return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        framer(url=build_url(netloc='localhost', port=8765),
               video_path='./data/video.mp4',
               output_path='./data/video-frames/',
               quality=95,
               processor=grayscale))
