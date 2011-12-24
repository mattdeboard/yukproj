from yuk.models import Item
from django.contrib import admin


class ItemAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'user', 'displays', 'item_type')

admin.site.register(Item, ItemAdmin)
