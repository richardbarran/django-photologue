from django.contrib import admin
from models import *

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('photos',)

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    search_fields = ['title', 'title_slug', 'caption']
    list_per_page = 10
    prepopulated_fields = {'title_slug': ('title',)}

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
        return False # To remove the 'Save and continue editing' button


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)
