from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm


admin.site.register(AboutUs)
admin.site.register(News, NewsAdmin)
admin.site.register(Help)
admin.site.register(Offer)
admin.site.register(Contacts)
admin.site.register(MainPageIcon)
admin.site.register(Advantages)