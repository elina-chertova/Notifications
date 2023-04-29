import asyncio
import websockets
from websocket.token_bucket import TokenBucket, MAX_MESSAGES_PER_SECOND, TOKENS_PER_SECOND

peoples = {}
client_buckets = {}
token_bucket = TokenBucket(MAX_MESSAGES_PER_SECOND, TOKENS_PER_SECOND)


async def welcome(websocket: websockets.WebSocketServerProtocol) -> str:
    await websocket.send('Представьтесь!')
    name = await websocket.recv()
    await websocket.send('Чтобы поговорить, напишите "<имя>: <сообщение>". Например: Ира: купи хлеб.')
    await websocket.send('Посмотреть список участников можно командой "?"')
    peoples[name.strip()] = websocket
    client_buckets[name.strip()] = TokenBucket(MAX_MESSAGES_PER_SECOND, TOKENS_PER_SECOND)
    return name


async def receiver(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    name = await welcome(websocket)
    while True:
        try:
            if token_bucket.consume_tokens(1):
                message = (await websocket.recv()).strip()
                if message == '?':
                    await websocket.send(', '.join(peoples.keys()))
                    continue
                elif ':' not in message:
                    await websocket.send('Неправильный формат команды')
                    continue
                else:
                    to, text = message.split(': ', 1)
                    if to in peoples:
                        await peoples[to].send(f'Сообщение от {name}: {text}')
                    else:
                        await websocket.send(f'Пользователь {to} не найден')
            else:
                await asyncio.sleep(0.1)

        except websockets.ConnectionClosed:
            print(f"Connection to {name} closed")
            del peoples[name.strip()]
            del client_buckets[name.strip()]

            break
        except Exception as e:
            print(f"Error {e}")
            break


ws_server = websockets.serve(receiver, "localhost", 8765)

loop = asyncio.get_event_loop()
loop.run_until_complete(ws_server)
loop.run_forever()
