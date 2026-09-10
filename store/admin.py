from django.contrib import admin
from .models import Product, Order, OrderItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'stock',
        'category',
        'created_at'
    )
    search_fields = ('name', 'category')
    list_filter = ('category',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'total_amount',
        'status',
        'created_at'
    )

    list_editable = ('status',)

    list_filter = (
        'status',
        'created_at'
    )

    search_fields = (
        'full_name',
        'phone',
        'user__username'
    )

    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order',
        'product',
        'quantity',
        'price'
    )

    search_fields = (
        'product__name',
        'order__user__username'
    )