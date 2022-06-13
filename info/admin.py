from functools import update_wrapper

from django.utils.html import format_html
from django.views.generic import RedirectView

from .models import AboutUs, News, Help, Offer, Contacts, MainPageIcon, Advantages, CallBack, \
    HelpIcon, HeaderFooterPic
from django import forms
from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdminUrl(admin.ModelAdmin):
    def change_view(self, request, object_id=None, form_url='', extra_context=None):
        try:
            id = self.model.objects.all().first().id
        except AttributeError:
            return self.changeform_view(request, None, form_url, extra_context)

        object_id = str(id)
        return self.changeform_view(request, object_id, form_url, extra_context)

    def get_urls(self):
        from django.urls import path

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)

            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name

        return [
            path('', wrap(self.change_view), name='%s_%s_changelist' % info),
            path('add/', wrap(self.add_view), name='%s_%s_add' % info),
            path('<path:object_id>/history/', wrap(self.history_view), name='%s_%s_history' % info),
            path('<path:object_id>/delete/', wrap(self.delete_view), name='%s_%s_delete' % info),
            path('<path:object_id>/change/', wrap(self.change_view), name='%s_%s_change' % info),
            # For backwards compatibility (was the change url before 1.9)
            path('<path:object_id>/', wrap(RedirectView.as_view(
                pattern_name='%s:%s_%s_change' % ((self.admin_site.name,) + info)
            ))),
        ]


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
class OfferAdmin(AdminUrl):
    form = OfferAdminForm

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(CallBack)
class CallBackAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'reason', 'call_status', 'date')
    list_filter = ('call_status', 'date')
    search_fields = ['name']


@admin.register(AboutUs)
class AboutUsAdmin(AdminUrl):

    class Meta:
        model = AboutUs

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(Contacts)
class ContactsAdmin(AdminUrl):

    class Meta:
        model = Contacts

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(HelpIcon)
class ContactsAdmin(admin.ModelAdmin):

    class Meta:
        model = HelpIcon

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="100px/>'.format(obj.icon.url))

    image_tag.short_description = 'icon'
    list_display = ['image_tag', ]

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(MainPageIcon)
class ContactsAdmin(admin.ModelAdmin):

    def image_tag(self, obj):
        return format_html('<img src="{}" width="auto" height="100px/>'.format(obj.icon.url))

    image_tag.short_description = 'icon'
    list_display = ['image_tag', ]

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


@admin.register(HeaderFooterPic)
class ContactsAdmin(AdminUrl):

    def has_add_permission(self, request):
        if self.model.objects.count() >= 1:
            return False
        return super().has_add_permission(request)


admin.site.register(Help)
admin.site.register(Advantages)
