from django.contrib import admin
from django import forms
from django.conf import settings

from .models import Gallery, Photo, GalleryUpload, PhotoEffect, PhotoSize, \
    Watermark

# Third party SortedManyToManyField may be used
# to allow user to adjust the order of photos in gallery
# (see https://pypi.python.org/pypi/django-sortedm2m)
USE_SORTEDM2M = getattr(settings, 'PHOTOLOGUE_USE_SORTEDM2M', False)

USE_CKEDITOR = getattr(settings, 'PHOTOLOGUE_USE_CKEDITOR', False)

if USE_CKEDITOR:
    from ckeditor.widgets import CKEditorWidget


class GalleryAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    if not USE_SORTEDM2M:
        filter_horizontal = ('photos',)
    form = GalleryAdminForm


class PhotoAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        caption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    search_fields = ['title', 'title_slug', 'caption']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}
    form = PhotoAdminForm


class PhotoEffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color', 'brightness', 'contrast', 'sharpness', 'filters', 'admin_sample')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Adjustments', {
            'fields': ('color', 'brightness', 'contrast', 'sharpness')
        }),
        ('Filters', {
            'fields': ('filters',)
        }),
        ('Reflection', {
            'fields': ('reflection_size', 'reflection_strength', 'background_color')
        }),
        ('Transpose', {
            'fields': ('transpose_method',)
        }),
    )


class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'effect', 'increment_count')
    fieldsets = (
        (None, {
            'fields': ('name', 'width', 'height', 'quality')
        }),
        ('Options', {
            'fields': ('upscale', 'crop', 'pre_cache', 'increment_count')
        }),
        ('Enhancements', {
            'fields': ('effect', 'watermark',)
        }),
    )


class WatermarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'opacity', 'style')


class GalleryUploadAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False  # To remove the 'Save and continue editing' button


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)
