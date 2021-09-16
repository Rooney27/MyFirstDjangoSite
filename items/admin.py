from django.contrib import admin
from .models import *



class OrderItemInline(admin.TabularInline):
    model = OrderItem
class PromotionItemInline(admin.TabularInline):
    model = PromotionItem

class ItemAdmin(admin.ModelAdmin):
    list_display = ['id','title', 'price']
    list_filter = ['category']
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'second_name',
                    'address', 'city', 'is_paid']
    list_filter = ['is_paid']
    inlines = [OrderItemInline]
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date',
                    'end_date']
    list_filter = ['start_date']
    inlines = [PromotionItemInline]
# Register your models here.
admin.site.register(Category)
admin.site.register(Item,ItemAdmin)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Promotion,PromotionAdmin)