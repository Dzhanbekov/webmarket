from .models import Collection, Item, ItemImageColor, ItemCart, Order, OrderItem, UserFavouriteItems
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ItemAdminForm(forms.ModelForm):
    """modelform for add ckeditor to item description"""

    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Item
        fields = '__all__'


class PhotoAdmin(admin.StackedInline):
    """class for add item image color model to item admin"""

    model = ItemImageColor
    max_num = 8


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    """register item model to django admin"""

    inlines = [PhotoAdmin]
    form = ItemAdminForm
    list_display = ['id', 'title', 'collection']
    list_display_links = ['id', 'title']
    list_filter = ['collection']

    class Meta:
        model = Item


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(UserFavouriteItems)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', 'user']
    list_display_links = ['id', 'item']


@admin.register(ItemCart)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'item', "amount_item", "amount"]
    list_display_links = ['id', 'item']


@admin.register(Order)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', "lastname", "phone_number", "country", "order_status", "created_at"]
    list_display_links = ['id', 'name']
    list_filter = ['country', "order_status", "created_at"]
    search_fields = ["name", "lastname"]


admin.site.register(OrderItem)
admin.site.site_header = "ZEON store Admin"
admin.site.site_title = "ZEON Admin Portal"
admin.site.index_title = "Welcome to ZEON STORE Portal"
