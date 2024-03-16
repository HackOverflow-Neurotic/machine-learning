import asyncio
import websockets

# Dictionary to store connected clients
clients = set()


# async def send_hello():
#     while True:
#         to_remove = set()  # Store disconnected clients to remove
#         for client in clients:
#             try:
#                 await client.send("Hello from server!")
#             except websockets.exceptions.ConnectionClosedError:
#                 to_remove.add(client)
#         # Remove disconnected clients
#         for client in to_remove:
#             clients.remove(client)
#         await asyncio.sleep(5)  # Send hello every 5 seconds


async def handle_client(websocket, path):
    # Register client
    clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received message: {message}")
            # Broadcast message to all clients
            for client in clients:
                await client.send(message)
    except websockets.exceptions.ConnectionClosedError:
        pass  # Handle the closed connection gracefully
    finally:
        # Unregister client when connection is closed
        clients.remove(websocket)


async def main():
    server = await websockets.serve(handle_client, "0.0.0.0", 8765)
    # Start the background task to send hello messages
    # asyncio.create_task(send_hello())
    # Keep the server running
    await server.wait_closed()


asyncio.run(main())
