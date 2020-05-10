from django.contrib import admin
from .models import Sliders, Item, Cart

# Register your models here.


class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Sliders)
admin.site.register(Item, ItemAdmin)
admin.site.register(Cart)
# admin.site.register(Transaction)