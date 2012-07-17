""" Newforms Admin configuration for Photologue

"""
from django.contrib.admin import ModelAdmin, site
from adminsortable.admin import SortableAdmin
from django import forms
from models import *


class GalleryAdmin(ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('photos',)

def crop_from_top(modeladmin, request, queryset):
    queryset.update(crop_from='top')
crop_from_top.short_description = "Crop photos from Top"

class PhotoAdmin(SortableAdmin):
    list_display = ('id', 'title', 'caption', 'tags', 'date_taken', 'date_added', 'is_public', 'view_count', 'admin_thumbnail')
    list_editable = ('title', 'caption', 'tags', 'is_public')
    list_filter = ['date_added', 'is_public', 'tags', 'galleries']
    search_fields = ['title', 'title_slug', 'caption', 'tags']
    prepopulated_fields = {'title_slug': ('title',)}
    actions = [crop_from_top]
    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(PhotoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'caption':
            formfield.widget = forms.Textarea(attrs={'cols': 60, 'rows': 2})
        return formfield

class PhotoEffectAdmin(ModelAdmin):
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

class PhotoSizeAdmin(ModelAdmin):
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


class WatermarkAdmin(ModelAdmin):
    list_display = ('name', 'opacity', 'style')


class GalleryUploadAdmin(ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False # To remove the 'Save and continue editing' button

class ImageOverrideInline(generic.GenericTabularInline):
    model = ImageOverride


site.register(Gallery, GalleryAdmin)
site.register(GalleryUpload)
site.register(Photo, PhotoAdmin)
site.register(PhotoEffect, PhotoEffectAdmin)
site.register(PhotoSize, PhotoSizeAdmin)
site.register(Watermark, WatermarkAdmin)
