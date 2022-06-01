from .models import Collection, Item, ItemImageColor, ItemCart, Order, SearchHelper
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ItemAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Item
        fields = '__all__'


class PhotoAdmin(admin.StackedInline):
    model = ItemImageColor
    max_num = 8


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin]
    form = ItemAdminForm

    class Meta:
        model = Item


admin.site.register(Collection)
admin.site.register(Order)
admin.site.register(ItemCart)
admin.site.register(SearchHelper)
