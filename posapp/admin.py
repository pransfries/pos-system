from django.contrib import admin
from .models import *

# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    list_display=['item_name', 'item_price', 'stock_quantity']

class OrderAdmin(admin.ModelAdmin):
    list_display=['total_amount', 'order_date', 'payment_type']

class ItemOrderAdmin(admin.ModelAdmin):
    list_display=['item_id', 'order_id', 'line_total', 'quantity']



admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder,ItemOrderAdmin)
