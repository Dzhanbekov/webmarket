from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class OfferAdminForm(forms.ModelForm):
    text = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Offer
        fields = '__all__'


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

    class Meta:
        model = News


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    form = OfferAdminForm

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'reason', 'call_status', 'date')
    list_filter = ('call_status', 'date')
    search_fields = ['name']


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):

    class Meta:
        model = AboutUs

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


admin.site.register(Help)
admin.site.register(Contacts)
admin.site.register(MainPageIcon)
admin.site.register(Advantages)
