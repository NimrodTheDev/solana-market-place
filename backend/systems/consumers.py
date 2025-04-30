import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Coin, Trade, UserCoinHoldings, SolanaUser
from django.db import transaction
from decimal import Decimal
from asgiref.sync import sync_to_async
from .listeners import SolanaEventListener

class SolanaConsumer(AsyncWebsocketConsumer):
    """
    Consumer for handling Solana WebSocket events and broadcasting them to connected clients
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        await self.accept()
        
        # Add to group
        await self.channel_layer.group_add(
            "solana_events",
            self.channel_name
        )
        
        # Start the Solana listener in a background task
        self.solana_listener_task = asyncio.create_task(self.start_solana_listener())
        
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Cancel the Solana listener task
        if hasattr(self, 'solana_listener_task') and self.solana_listener_task:
            self.solana_listener_task.cancel()
            
        # Remove from group
        await self.channel_layer.group_discard(
            "solana_events",
            self.channel_name
        )
        
        # Close Solana connection if it exists
        if hasattr(self, 'solana_listener') and self.solana_listener:
            await self.solana_listener.close()
    
    async def receive(self, text_data):
        """Handle messages from WebSocket"""
        data = json.loads(text_data)
        command = data.get('command')
        
        if command == 'subscribe_program':
            program_id = data.get('program_id')
            if program_id:
                # Implement logic to subscribe to a specific program
                await self.send(text_data=json.dumps({
                    'message': f'Subscribed to program {program_id}'
                }))
    
    async def start_solana_listener(self):
        """Initialize and start the Solana event listener"""
        try:
            # Use devnet or mainnet depending on your needs
            rpc_ws_url = "wss://api.devnet.solana.com"
            
            # Replace with your actual program ID
            program_id = "YOUR_PROGRAM_ID_HERE"
            
            # Create and initialize listener
            self.solana_listener = SolanaEventListener(
                rpc_ws_url, 
                program_id,
                callback=self.process_solana_event
            )
            
            # Connect and subscribe
            await self.solana_listener.connect()
            await self.solana_listener.subscribe_program_logs()
            
            # Keep the task alive
            while True:
                await asyncio.sleep(1)
                
        except asyncio.CancelledError:
            # Handle task cancellation
            if hasattr(self, 'solana_listener'):
                await self.solana_listener.close()
            raise
        except Exception as e:
            # Log any errors
            print(f"Error in Solana listener: {e}")
            import traceback
            traceback.print_exc()
    
    async def process_solana_event(self, event_data):
        """Process Solana program events and update database"""
        try:
            # Extract key information
            signature = event_data.get('signature')
            logs = event_data.get('logs', [])
            
            # Process logs to extract relevant information
            event_type = None
            coin_address = None
            user_wallet = None
            coin_amount = None
            sol_amount = None
            
            # Parse logs to extract information
            # This parsing logic will depend on your specific program's log format
            for log in logs:
                # Example parsing logic - adjust based on your program's log format
                if "Event: COIN_CREATE" in log:
                    event_type = "COIN_CREATE"
                    # Extract coin address from log
                    # This is just an example - adjust based on your log format
                    coin_address = self.extract_address_from_log(log)
                    
                elif "Event: BUY" in log:
                    event_type = "BUY"
                    # Extract trade details
                    coin_address, user_wallet, coin_amount, sol_amount = self.extract_trade_details(log)
                    
                elif "Event: SELL" in log:
                    event_type = "SELL"
                    # Extract trade details
                    coin_address, user_wallet, coin_amount, sol_amount = self.extract_trade_details(log)
            
            # Process the event based on its type
            if event_type and signature:
                if event_type == "COIN_CREATE" and coin_address:
                    # Handle coin creation
                    await self.handle_coin_creation(signature, coin_address)
                    
                elif event_type in ["BUY", "SELL"] and all([coin_address, user_wallet, coin_amount, sol_amount]):
                    # Handle trade
                    await self.handle_trade(signature, event_type, coin_address, user_wallet, coin_amount, sol_amount)
                
                # Broadcast event to all connected clients
                await self.channel_layer.group_send(
                    "solana_events",
                    {
                        "type": "broadcast_event",
                        "event_type": event_type,
                        "signature": signature,
                        "details": {
                            "coin_address": coin_address,
                            "user_wallet": user_wallet,
                            "coin_amount": str(coin_amount) if coin_amount else None,
                            "sol_amount": str(sol_amount) if sol_amount else None,
                        }
                    }
                )
        except Exception as e:
            print(f"Error processing Solana event: {e}")
            import traceback
            traceback.print_exc()
    
    def extract_address_from_log(self, log):
        """Extract address from log - customize based on your log format"""
        # Example implementation - adjust based on your log format
        # For example, if your log contains "Address: ABC123"
        if "Address:" in log:
            return log.split("Address:")[1].strip().split()[0]
        return None
    
    def extract_trade_details(self, log):
        """Extract trade details from log - customize based on your log format"""
        # Example implementation - adjust based on your log format
        # This should extract coin_address, user_wallet, coin_amount, sol_amount
        # Return as tuple (coin_address, user_wallet, coin_amount, sol_amount)
        # Example placeholder - you need to implement based on your log format
        return None, None, None, None
    
    @sync_to_async
    def handle_coin_creation(self, signature, coin_address):
        """Handle coin creation event"""
        # Check if coin already exists
        if not Coin.objects.filter(address=coin_address).exists():
            # Create new coin record
            # Note: You'll need more data from the logs for a complete coin record
            new_coin = Coin(
                address=coin_address,
                # Add other required fields
            )
            new_coin.save()
            print(f"Created new coin with address: {coin_address}")
    
    @sync_to_async
    def handle_trade(self, signature, trade_type, coin_address, user_wallet, coin_amount, sol_amount):
        """Handle trade event (BUY or SELL)"""
        # Check if trade already exists
        if not Trade.objects.filter(transaction_hash=signature).exists():
            with transaction.atomic():
                # Get or create coin
                coin, _ = Coin.objects.get_or_create(address=coin_address)
                
                # Get or create user
                user, _ = SolanaUser.objects.get_or_create(wallet_address=user_wallet)
                
                # Create trade record
                trade = Trade(
                    transaction_hash=signature,
                    user=user,
                    coin=coin,
                    trade_type=trade_type,
                    coin_amount=Decimal(coin_amount),
                    sol_amount=Decimal(sol_amount),
                )
                trade.save()
                
                # Update user coin holdings
                holding, created = UserCoinHoldings.objects.get_or_create(
                    user=user,
                    coin=coin,
                    defaults={'amount': 0}
                )
                
                # Update amount based on trade type
                if trade_type == 'BUY':
                    holding.amount += Decimal(coin_amount)
                elif trade_type == 'SELL':
                    holding.amount -= Decimal(coin_amount)
                
                holding.save()
                print(f"Processed {trade_type} trade: {signature}")
    
    async def broadcast_event(self, event):
        """Broadcast event to WebSocket clients"""
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'event_type': event['event_type'],
            'signature': event['signature'],
            'details': event['details']
        }))

