from .models import Collection, Item, ItemImage, ItemColor
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class ItemAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Item
        fields = '__all__'


class PhotoAdmin(admin.StackedInline):
    model = ItemImage


class ColorAdmin(admin.StackedInline):
    model = ItemColor


class ItemAdmin(admin.ModelAdmin):
    inlines = [PhotoAdmin, ColorAdmin]
    form = ItemAdminForm

    class Meta:
        model = Item


admin.site.register(Collection)
admin.site.register(Item, ItemAdmin)
# admin.site.register(ItemImage)
# admin.site.register(ItemColor)
