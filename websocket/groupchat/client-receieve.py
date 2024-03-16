import asyncio
import websockets


async def send_message():
    async with websockets.connect("ws://0.0.0.0:8765", ping_timeout=300) as websocket:
        while True:
            message = input("Enter your message: ")
            await websocket.send(message)


async def receive_message():
    async with websockets.connect("ws://0.0.0.0:8765", ping_timeout=300) as websocket:
        while True:
            message = await websocket.recv()
            print("Received message:", message)


asyncio.run(receive_message())
