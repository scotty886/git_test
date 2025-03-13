from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem

# Register your models here.

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

# Create an OrderItem Inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0
# Extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    fields = ["user", "full_name", "email", "shipping_address", "amount_paid", "date_ordered", "date_shipped", "shipped"]
    inlines = [OrderItemInline]

admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)



