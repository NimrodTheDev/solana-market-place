from django.test import TestCase

# Create your tests here.


# from django.test import TestCase

# # Create your tests here.
# import json
# import asyncio
# import unittest
# from unittest.mock import patch, AsyncMock

# from channels.testing import WebsocketCommunicator
# from django.test import TransactionTestCase
# from solana_listeners.asgi import application


# class SolanaConsumerTests(TransactionTestCase):
#     """
#     Test case for SolanaConsumer using Django unittest and Channels
#     """
#     # Required for Channels tests to run correctly
#     databases = '__all__'

#     @patch("solana_listener.consumers.SolanaEventListener")
#     def test_websocket_connect_and_subscribe(self, mock_listener):
#         async def inner():
#             # Mock listener so we don’t make real WebSocket connections
#             mock_instance = AsyncMock()
#             mock_listener.return_value = mock_instance

#             communicator = WebsocketCommunicator(application, "/ws/solana/")
#             connected, _ = await communicator.connect()
#             self.assertTrue(connected)

#             # Send a subscribe message
#             await communicator.send_json_to({
#                 "command": "subscribe_program",
#                 "program_id": "mock_program"
#             })

#             response = await communicator.receive_json_from()
#             self.assertEqual(response, {
#                 "message": "Subscribed to program mock_program"
#             })

#             await communicator.disconnect()

#         asyncio.run(inner())

#     @patch("solana_listener.consumers.SolanaEventListener")
#     def test_websocket_broadcast_event(self, mock_listener):
#         async def inner():
#             mock_instance = AsyncMock()
#             mock_listener.return_value = mock_instance

#             communicator = WebsocketCommunicator(application, "/ws/solana/")
#             connected, _ = await communicator.connect()
#             self.assertTrue(connected)

#             # Simulate a group broadcast
#             from channels.layers import get_channel_layer
#             channel_layer = get_channel_layer()
#             await channel_layer.group_send("solana_events", {
#                 "type": "broadcast_event",
#                 "event_type": "BUY",
#                 "signature": "tx123",
#                 "details": {
#                     "coin_address": "coinABC",
#                     "user_wallet": "walletXYZ",
#                     "coin_amount": "10.5",
#                     "sol_amount": "0.25"
#                 }
#             })

#             # Validate response received by WebSocket client
#             response = await communicator.receive_json_from()
#             self.assertEqual(response["event_type"], "BUY")
#             self.assertEqual(response["signature"], "tx123")
#             self.assertEqual(response["details"]["coin_address"], "coinABC")

#             await communicator.disconnect()

#         asyncio.run(inner())
