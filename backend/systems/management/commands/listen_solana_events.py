import asyncio
from django.core.management.base import BaseCommand
from systems.consumers import SolanaEventListener
from systems.models import Coin, Trade, UserCoinHoldings, SolanaUser
from asgiref.sync import sync_to_async
from decimal import Decimal

class Command(BaseCommand):
    help = 'Listen for Solana program events'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Solana event listener...'))
        asyncio.run(self.run_listener())

    async def run_listener(self):
        # Setup your event listener similar to the consumer code
        rpc_ws_url = "wss://api.devnet.solana.com"
        program_id = "A7sBBSngzEZTsCPCffHDbeXDJ54uJWkwdEsskmn2YBGo"
        
        listener = SolanaEventListener(
            rpc_ws_url, 
            program_id,
            callback=self.process_event
        )
        
        try:
            await listener.connect()
            await listener.subscribe_program_logs()
            
            # Keep running indefinitely
            while True:
                await asyncio.sleep(1)
                
        except KeyboardInterrupt:
            self.stdout.write(self.style.WARNING('Shutting down listener...'))
            await listener.close()
    
    async def process_event(self, event_data):
        print(event_data)
        # Implement logic similar to the consumer
        ...