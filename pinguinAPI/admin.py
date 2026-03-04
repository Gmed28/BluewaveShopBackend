from django.contrib import admin
from .models import Product, Stock
 
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_id", "product_name", "price",)  # anpassen, falls du Felder änderst
    search_fields = ("product_name",)
    list_filter = ("price",)
 
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "amount")
    search_fields = ("product__product_name",)