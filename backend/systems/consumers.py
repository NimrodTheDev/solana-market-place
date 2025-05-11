from channels.generic.websocket import AsyncJsonWebsocketConsumer

class RealTimeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add(
            "events",
            self.channel_name
        )
        print("connected")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "events",
            self.channel_name
        )
    
    async def solana_event(self, event):
        """
        Handler for messages sent directly via channel layer
        """
        await self.send_json(event.get('data'))
