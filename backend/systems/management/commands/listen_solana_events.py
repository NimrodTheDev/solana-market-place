import asyncio
from django.core.management.base import BaseCommand
from systems.consumers import SolanaEventListener
from systems.models import Coin, Trade, SolanaUser, DeveloperScore
from asgiref.sync import sync_to_async
from decimal import Decimal
from systems.parser import TokenEventDecoder

class Command(BaseCommand):
    help = 'Listen for Solana program events'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Solana event listener...'))
        asyncio.run(self.run_listener())

    async def run_listener(self):
        # Setup your event listener similar to the consumer code
        rpc_ws_url = "wss://api.devnet.solana.com"
        program_id = "5ZzjiqegSE2sGSSDpHr4eaYN4gTYdKW6N9JAVPWAyn2s"
        
        listener = SolanaEventListener(
            rpc_ws_url=rpc_ws_url,
            program_id=program_id,
            callback=self.process_event,
            max_retries=None,  # Infinite retries
            retry_delay=3,
            auto_restart=True
        )
        self.decoders = {}
        self.decoders["CreateToken"] = TokenEventDecoder(
            "TokenCreatedEvent", {
                "token_name": "string",
                "token_symbol": "string",
                "token_uri": "string",
                "mint_address": "pubkey",
                "metadata_address": "pubkey",
                "authority": "pubkey",
                "decimals": "u8",
            }
        )
        try:
            # Start the listener with auto-restart enabled
            await listener.listen()
        except KeyboardInterrupt:
            print("Keyboard interrupt received")
        finally:
            # Gracefully shut down
            await listener.stop()
    
    async def process_event(self, event_data):
        # This handles both dict and dot-access objects
        # check the type
        signature = getattr(event_data, 'signature', None)
        logs = getattr(event_data, 'logs', [])

        event_type, currect_log = self.get_function_id(logs)
        if event_type and signature:
            if event_type == "CreateToken":
                if event_type in self.decoders:
                    for log in logs[currect_log:]:
                        event = self.decoders[event_type].decode(log)
                        if event:
                            await self.handle_coin_creation(signature, event)
                            break
    
    @sync_to_async
    def handle_coin_creation(self, signature, logs):
        """Handle coin creation event"""
        creator = None
        try:
            print(logs["authority"])
            creator = SolanaUser.objects.get(wallet_address=str(logs["authority"]).lower())
        except SolanaUser.DoesNotExist:
            print("Creator not found.")

        if not Coin.objects.filter(address=logs["mint_address"]).exists() and creator != None:
            ds = DeveloperScore.objects.get_or_create(developer=creator)
            # Create new coin record
            # Note: You'll need more data from the logs for a complete coin record
            new_coin = Coin(
                address=logs["mint_address"],
                name= logs["token_name"],
                ticker=logs["token_symbol"],
                creator=creator,
                total_supply=Decimal("1000000.0"),
                image_url="https://example.com3/coin.png",
                current_price=Decimal("1.0")
            )
            new_coin.save()
            ds.recalculate_score()
            print(f"Created new coin with address: {logs["mint_address"]}")
            print("Tx Signature:", signature)

    def get_function_id(self, logs:list) -> tuple:
        for num, log in enumerate(logs): # get the function id
            if "Program log: Instruction:" in log:
                return log.split(": ")[-1], num
        