import asyncio
import websockets
import json
from typing import Callable

class KuafuBot:
    def __init__(self, uri: str):
        self.ws_uri = f'ws://{uri}'
        self.command_handler = None
        self.command_str = None
        self.loop = asyncio.get_event_loop()

    def command(self, command_str: str):
        def decorator(func: Callable):
            self.command_handler = func
            self.command_str = command_str
            self.ws_uri = self.ws_uri + '/' + command_str
            return func
        return decorator

    async def handle_message(self, message: str):
        if self.command_handler:
            response_msg = await self.command_handler(message)
            return response_msg
        else:
            print("No command handler set.")

    async def connect_and_listen(self):
        async with websockets.connect(self.ws_uri) as websocket:
            while True:
                message = await websocket.recv()
                data = json.loads(message)
                msg = data['msg']
                incoming = data['incoming']
                response_msg = await self.handle_message(msg)
                if response_msg:
                    await websocket.send(json.dumps({'incoming': incoming, 'msg': response_msg}))

    def run(self):
        if self.command_str is None:
            raise Exception("No command defined for the bot.")
        self.loop.run_until_complete(self.connect_and_listen())