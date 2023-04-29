
import asyncio

import websockets


async def send_messages():
    async with websockets.connect("ws://localhost:8765") as websocket:
        while True:
            for i in range(10):
                message = f"Spammer: Message {i+1}"
                await websocket.send(message)
                print(f">>> {message}")
                await asyncio.sleep(0.1)

asyncio.get_event_loop().run_until_complete(send_messages())

