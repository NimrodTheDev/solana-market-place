from solana.rpc.websocket_api import connect, RpcTransactionLogsFilterMentions 
from solders.pubkey import Pubkey 
import asyncio
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SolanaEventListener: 
    def __init__(self, rpc_ws_url, program_id, callback=None, commitment='confirmed',
                 max_retries=10, retry_delay=5, auto_restart=True): 
        """ 
        Initialize the Solana event listener with auto-restart capability. 
         
        Args: 
            rpc_ws_url (str): Solana WebSocket RPC URL 
            program_id (str): The program ID to monitor for events 
            callback (callable): Function to call when logs are received 
            commitment (str): Commitment level (processed, confirmed, finalized)
            max_retries (int): Maximum number of reconnection attempts (None for infinite)
            retry_delay (int): Delay in seconds between retry attempts
            auto_restart (bool): Whether to automatically restart on failure
        """ 
        self.rpc_ws_url = rpc_ws_url 
        self.program_id = Pubkey.from_string(program_id) 
        self.commitment = commitment 
        self.callback = callback 
        self.subscription_id = None 
        self.ws_connection = None
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.auto_restart = auto_restart
        self.should_run = False
        self.retry_count = 0
         
    async def connect(self): 
        """Establish connection to Solana WebSocket endpoint""" 
        try:
            self.ws_connection = await connect(self.rpc_ws_url) 
            logger.info(f"Connected to Solana WebSocket at {self.rpc_ws_url}")
            # Reset retry count on successful connection
            self.retry_count = 0
            return True
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            return False
         
    async def subscribe_program_logs(self): 
        """Subscribe to program logs.""" 
        if not self.ws_connection: 
            success = await self.connect()
            if not success:
                return False
         
        try:
            # Create a proper filter object for the program ID 
            program_filter = RpcTransactionLogsFilterMentions(self.program_id) 
             
            # Subscribe to program logs 
            subscription_id = await self.ws_connection.logs_subscribe( 
                program_filter, 
                self.commitment 
            ) 
            
            self.subscription_id = subscription_id 
            logger.info(f"Subscribed to logs for program {self.program_id}")
            return True
        except Exception as e:
            logger.error(f"Subscription failed: {e}")
            return False
    
    async def process_messages(self):
        """Process incoming messages from websocket"""
        if not self.ws_connection:
            return False
            
        try:
            async for msg in self.ws_connection: 
                if not self.should_run:
                    break
                    
                logger.debug(f"Received message: {msg}") 
                print(type(msg))
                 
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
            
            return True
        except Exception as e:
            logger.error(f"Error processing messages: {e}")
            import traceback
            traceback.print_exc()
            return False

    async def listen(self):
        """Main method to start the listener with auto-restart capability"""
        self.should_run = True
        
        while self.should_run:
            try:
                # Connect and subscribe
                subscription_success = await self.subscribe_program_logs()
                if not subscription_success:
                    raise Exception("Failed to subscribe to program logs")
                
                # Process messages
                processing_success = await self.process_messages()
                if not processing_success:
                    raise Exception("Message processing failed")
                
            except Exception as e:
                logger.error(f"Listener error: {e}")
                # Clean up existing connection
                await self.close(unsubscribe=True)
                
                if not self.auto_restart:
                    logger.info("Auto-restart disabled. Exiting.")
                    break
                
                # Implement exponential backoff
                self.retry_count += 1
                if self.max_retries is not None and self.retry_count > self.max_retries:
                    logger.error(f"Maximum retry attempts ({self.max_retries}) reached. Stopping.")
                    break
                    
                backoff_time = min(self.retry_delay * (2 ** (self.retry_count - 1)), 60)  # Cap at 60 seconds
                logger.info(f"Attempting to restart in {backoff_time} seconds (retry {self.retry_count}/{self.max_retries if self.max_retries else 'unlimited'})")
                await asyncio.sleep(backoff_time)
            
    async def stop(self):
        """Stop the listener gracefully"""
        logger.info("Stopping listener...")
        self.should_run = False
        await self.close()
        
    async def unsubscribe(self): 
        """Unsubscribe from program logs""" 
        if self.ws_connection and self.subscription_id: 
            try:
                await self.ws_connection.logs_unsubscribe(self.subscription_id) 
                logger.info(f"Unsubscribed from logs (ID: {self.subscription_id})") 
            except Exception as e:
                logger.warning(f"Error unsubscribing: {e}")
            finally:
                self.subscription_id = None 
     
    async def close(self, unsubscribe=True): 
        """Close WebSocket connection""" 
        if unsubscribe and self.subscription_id: 
            await self.unsubscribe() 
         
        if self.ws_connection: 
            try:
                await self.ws_connection.close() 
                logger.info("WebSocket connection closed") 
            except Exception as e:
                logger.warning(f"Error closing connection: {e}")
            finally:
                self.ws_connection = None

# Example usage:
async def example_log_callback(log_data):
    logger.info(f"Received log data: {log_data}")

async def run_example():
    # Replace with your values
    rpc_ws_url = "wss://api.mainnet-beta.solana.com"
    program_id = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"  # Token Program
    
    listener = SolanaEventListener(
        rpc_ws_url=rpc_ws_url,
        program_id=program_id,
        callback=example_log_callback,
        max_retries=None,  # Infinite retries
        retry_delay=3,
        auto_restart=True
    )
    
    try:
        # Start the listener with auto-restart enabled
        await listener.listen()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received")
    finally:
        # Gracefully shut down
        await listener.stop()

if __name__ == "__main__":
    # Run the example
    asyncio.run(run_example())