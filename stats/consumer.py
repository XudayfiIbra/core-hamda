from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Statistic, DataItem


class DashboardConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.slug = self.scope['url_route'].get('kwargs', {}).get('slug')
        if self.slug:
            self.room_group_name = f'stats-{self.slug}'
        else:
            self.room_group_name = 'default_stats'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        print(f'Connection closed with code: {close_code}')
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive_json(self, content, **kwargs):
        message = content.get('message')
        sender = content.get('sender')

        slug = self.slug

        await self.save_data_item(sender, message, slug)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'statistics_message',
                'message': message,
                'sender': sender
            }
        )

    async def statistics_message(self, event):
        message = event['message']
        sender = event['sender']

        await self.send_json({
            'message': message,
            'sender': sender
        })

    @database_sync_to_async
    def create_data_item(self, message, sender, slug):
        obj = Statistic.objects.filter(slug=slug).first()
        if obj:
            return DataItem.objects.create(
                statistic=obj,
                value=message,
                owner="test owner"
            )
        else:
            return None

    async def save_data_item(self, sender, message, slug):
        await self.create_data_item(message, sender, slug)
