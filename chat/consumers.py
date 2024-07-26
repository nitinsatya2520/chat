import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']

        if not self.user.is_authenticated:
            await self.close()
            return

        self.room_group_name = f'chat_{self.username}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(f"Received message: {message}")

        try:
            receiver = User.objects.get(username=self.username)
            Message.objects.create(sender=self.user, receiver=receiver, content=message)
            print(f"Message saved: {message}")
        except ObjectDoesNotExist:
            await self.send(text_data=json.dumps({
                'message': 'User not found',
                'sender': 'system',
            }))
            return

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )
        print(f"Message sent to group: {message}")

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']

        print(f"Sending message to WebSocket: {message} from {sender}")

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
        }))
