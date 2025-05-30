from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from systems.models import Coin, Trade

def _broadcast(info: dict, group: str = "events"):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        group,
        {
            "type": "solana_event",
            "data": info,
        }
    )

def broadcast_coin_created(instance: Coin):
    coin_info = {
        "address": instance.address,
        "name": instance.name,
        "ticker": instance.ticker,
        "creator": instance.creator.wallet_address,
        "total_supply": str(instance.total_supply),
        "image_url": instance.image_url,
        "current_price": str(instance.current_price),
        "description": instance.description,
        "discord": instance.discord,
        "website": instance.website,
        "twitter": instance.twitter,
    }
    _broadcast(coin_info)

def broadcast_trade_created(instance: Trade):
    trade_info = {
        "transaction_hash": instance.transaction_hash,
        "user": instance.user.wallet_address,
        "coin_address": instance.coin.address,
        "trade_type": instance.trade_type,
        "coin_amount": str(instance.coin_amount),
        "sol_amount": str(instance.sol_amount),
    }
    _broadcast(trade_info)   
