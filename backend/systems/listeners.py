from solana.rpc.websocket_api import connect, RpcTransactionLogsFilterMentions
from solders.pubkey import Pubkey

class SolanaEventListener:
    def __init__(self, rpc_ws_url, program_id, callback=None, commitment='confirmed'):
        """
        Initialize the Solana event listener.
        
        Args:
            rpc_ws_url (str): Solana WebSocket RPC URL
            program_id (str): The program ID to monitor for events
            callback (callable): Function to call when logs are received
            commitment (str): Commitment level (processed, confirmed, finalized)
        """
        self.rpc_ws_url = rpc_ws_url
        self.program_id = Pubkey.from_string(program_id)
        self.commitment = commitment
        self.callback = callback
        self.subscription_id = None
        self.ws_connection = None
        
    async def connect(self):
        """Establish connection to Solana WebSocket endpoint"""
        self.ws_connection = await connect(self.rpc_ws_url)
        print(f"Connected to Solana WebSocket at {self.rpc_ws_url}")
        
    async def subscribe_program_logs(self):
        """Subscribe to program logs."""
        if not self.ws_connection:
            await self.connect()
        
        # Create a proper filter object for the program ID
        program_filter = RpcTransactionLogsFilterMentions(self.program_id)
        
        # Subscribe to program logs
        subscription_id = await self.ws_connection.logs_subscribe(
            program_filter,
            self.commitment
        )
        
        self.subscription_id = subscription_id
        print(f"Subscribed to logs for program {self.program_id}")
        
        # Start listening for events
        try:
            async for msg in self.ws_connection:
                print(f"Received message: {msg}")
                
                # Handle subscription response
                if hasattr(msg, 'result') and not hasattr(msg, 'method'):
                    # This is likely the subscription confirmation
                    continue
                    
                # Check if it's a notification with logs
                if hasattr(msg, 'method') and msg.method == "logsNotification":
                    if self.callback:
                        await self.callback(msg.params.result.value)
                elif isinstance(msg, dict) and msg.get('method') == "logsNotification":
                    if self.callback:
                        await self.callback(msg.get('params', {}).get('result', {}).get('value', {}))
                elif isinstance(msg, list):
                    # Process list-type messages that might contain notification data
                    for item in msg:
                        if isinstance(item, dict) and item.get('method') == "logsNotification":
                            if self.callback:
                                await self.callback(item.get('params', {}).get('result', {}).get('value', {}))
                            
        except Exception as e:
            print(f"Error in event listener: {e}")
            import traceback
            traceback.print_exc()
        
    async def unsubscribe(self):
        """Unsubscribe from program logs"""
        if self.ws_connection and self.subscription_id:
            await self.ws_connection.logs_unsubscribe(self.subscription_id)
            print(f"Unsubscribed from logs (ID: {self.subscription_id})")
            self.subscription_id = None
    
    async def close(self):
        """Close WebSocket connection"""
        if self.subscription_id:
            await self.unsubscribe()
        
        if self.ws_connection:
            await self.ws_connection.close()
            print("WebSocket connection closed")
            self.ws_connection = None