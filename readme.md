# Video pipeline

A simple Python websocket client-server demo. The client takes a video input at
`/client/data/video.mp4`, decomposes it into frames (stored in `/client/data/video-frames/*.jpg`),
and forwards them to the server. The server will store all incoming images at
`/server/*.jpg`.

By default, the server is running on `ws://localhost:8765`.

## Requirements

- Python 3.7
- Other dependencies can be installed via `pip install -r requirements.txt`

## Usage

- To run the server: `python server.py`
- To run the client: `python client.py`
