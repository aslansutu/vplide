import json

from channels.generic.websocket import AsyncWebsocketConsumer


class DebuggerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.debugname = self.scope["url_route"]["kwargs"]["debug_name"]
        self.debug_group_name = "debug_%s" % self.debug_name

        await self.channel_layer.group_add(self.debug_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.debug_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.channel_layer.group_send(
            self.debug_group_name, {"type": "debug_message", "message": message}
        )

    async def debug_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"message": message}))
