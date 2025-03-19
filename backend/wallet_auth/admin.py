# wallet_auth/admin.py

from django.contrib import admin
from .models import SolanaUser, Coin, UserCoinHoldings, Trade

@admin.register(SolanaUser)
class SolanaUserAdmin(admin.ModelAdmin):
    list_display = ('wallet_address', 'display_name', 'is_staff', 'is_superuser')
    search_fields = ('wallet_address', 'display_name')
    list_filter = ('is_staff', 'is_superuser')

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'creator', 'created_at', 'current_price')
    search_fields = ('symbol', 'name', 'address')
    list_filter = ('created_at',)
    readonly_fields = ('address',)  # Make address read-only in the admin
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to set the address field if it's not provided
        This ensures we always have a valid address for coins created in the admin
        """
        if not obj.address:
            # Generate a unique address if one is not provided
            import uuid
            obj.address = f"COIN_{uuid.uuid4().hex[:40]}"
        
        # Set creator to the current admin user if not already set
        if not obj.creator_id:
            obj.creator = request.user
            
        super().save_model(request, obj, form, change)

@admin.register(UserCoinHoldings)
class UserCoinHoldingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'coin', 'amount_held')
    search_fields = ('user__wallet_address', 'coin__symbol')
    list_filter = ('coin',)

@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'coin', 'trade_type_display', 'coin_amount', 'sol_amount', 'created_at')
    search_fields = ('user__wallet_address', 'coin__symbol')
    list_filter = ('trade_type', 'created_at')
    readonly_fields = ('id',)
    
    def trade_type_display(self, obj):
        return "Buy" if obj.trade_type else "Sell"
    trade_type_display.short_description = "Trade Type"