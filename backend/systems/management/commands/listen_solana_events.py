import asyncio
from django.core.management.base import BaseCommand
from systems.listeners import SolanaEventListener
from systems.models import Coin, Trade, SolanaUser
from decimal import Decimal
from systems.parser import TokenEventDecoder
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync, sync_to_async
import requests

class Command(BaseCommand):
    help = 'Listen for Solana program events'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Solana event listener...'))
        asyncio.run(self.run_listener())

    async def run_listener(self):
        # Setup your event listener similar to the consumer code
        rpc_ws_url = "wss://api.devnet.solana.com"
        program_id = "443aQT61EYaeiqqdqGth95LYgfQkZF1BQbaJLZJ6i29w"
        
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
                "creator": "pubkey",
                "decimals": "u8",
            }
        )
        trade_decoder = TokenEventDecoder(
            "TokenTransferEvent", {
                "transfer_type": "u8",
                "mint_address": "pubkey",
                "user": "pubkey",
                "sol_amount": "u64",
                "coin_amount": "u64",
            }
        )
        self.decoders["BuyToken"] = trade_decoder
        self.decoders["SellToken"] = trade_decoder
        
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
                            event = await self.get_metadata(event)
                            await self.handle_coin_creation(signature, event)
                            break
            if event_type in ["SellToken", "BuyToken"]:
                if event_type in self.decoders:
                    for log in logs[currect_log:]:
                        event = self.decoders[event_type].decode(log)
                        if event:
                            await self.handle_trade(signature, event)
                            break

    @sync_to_async
    def handle_coin_creation(self, signature: str, logs: dict):
        """Handle coin creation event"""
        creator = None
        try:
            creator = SolanaUser.objects.get(wallet_address=logs["creator"])
        except SolanaUser.DoesNotExist:
            print("Creator not found.")
        
        if not Coin.objects.filter(address=logs["mint_address"]).exists() and creator is not None:
            attributes = logs.get('attributes')
            coin_info = {
                "address":logs["mint_address"],
                "name":logs["token_name"],
                "ticker":logs["token_symbol"],
                "creator":logs["creator"],
                "total_supply":"1000000.0",
                "image_url":logs.get('image', ''),
                "current_price":"1.0",
                "description":logs.get('description', None),
                "discord":attributes.get('discord') if isinstance(attributes, dict) else None,
                "website":attributes.get('website') if isinstance(attributes, dict) else None,
                "twitter":attributes.get('twitter') if isinstance(attributes, dict) else None,
            }
            new_coin = Coin(
                address=coin_info["address"],
                name=coin_info["name"],
                ticker=coin_info["ticker"],
                creator=creator,
                total_supply=Decimal(coin_info["total_supply"]),
                image_url=coin_info["image_url"],
                current_price=Decimal(coin_info["current_price"]),
                description=coin_info["description"],
                discord=coin_info["discord"],
                website=coin_info["website"],
                twitter=coin_info["twitter"],
            )
            new_coin.save()
            
            print(f"Created new coin with address: {logs['mint_address']}")
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "events",  # Group name
                {
                    "type": "solana_event",
                    'data': coin_info,
                }
            )

    async def get_metadata(self, log:dict):
        try:
            ipfuri:str = log["token_uri"]
            ipfs_hash = ipfuri.split("/")
            for i in range(2):
                if ipfs_hash[-(i+1)] != "":
                    ipfs_hash = ipfs_hash[-(i+1)]
                    break
            url = f"https://ipfs.io/ipfs/{ipfs_hash}"

            response = requests.get(url)

            if response.status_code == 200:
                content:dict = response.json()  # raw bytes
                log.update(content)
            else:
                print(f"Failed to fetch: {response.status_code}")
        except Exception as e:
            print(e)
        return log
    
    @sync_to_async
    def handle_trade(self, signature, logs):
        """Handle coin creation event"""
        tradeuser = None
        try:
            tradeuser = SolanaUser.objects.get(wallet_address=logs["user"])
        except SolanaUser.DoesNotExist:
            print("Creator not found.")
        
        coin = None
        try:
            coin = Coin.objects.get(address=logs["mint_address"])
        except Coin.DoesNotExist:
            print("Coins not found.")

        if not Trade.objects.filter(transaction_hash=signature).exists() and tradeuser != None and coin != None:
            trade_info = {
                "transaction_hash":signature,
                "user":logs["user"],
                "coin_address":logs["mint_address"],
                "trade_type":self.get_transaction_type(logs["transfer_type"]),
                "coin_amount":logs["coin_amount"],
                "sol_amount":logs["sol_amount"],
            }
            new_trade = Trade(
                transaction_hash=trade_info["transaction_hash"],
                user= tradeuser,
                coin=coin,
                trade_type=trade_info["trade_type"],
                coin_amount=trade_info["coin_amount"],
                sol_amount=trade_info["sol_amount"],
            )
            new_trade.save()
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "events",  # Group name
                {
                    "type": "solana_event",
                    'data': trade_info,
                }
            )
            print(f"Created new trade with transaction_hash: {signature}")

    def get_transaction_type(self, ttype):
        ttype = str(ttype)
        if ttype == "1":
            return "SELL"
        if ttype == "2":
            return "COIN_CREATE"
        if ttype == "0":
            return "BUY"
        raise(ValueError("Type not Registered"))

    def get_function_id(self, logs:list) -> tuple:
        for num, log in enumerate(logs): # get the function id
            if "Program log: Instruction:" in log:
                return log.split(": ")[-1], num
