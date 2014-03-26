from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib import messages
from django.utils.translation import ungettext

from .models import Gallery, Photo, GalleryUpload, PhotoEffect, PhotoSize, \
    Watermark

USE_CKEDITOR = getattr(settings, 'PHOTOLOGUE_USE_CKEDITOR', False)

if USE_CKEDITOR:
    from ckeditor.widgets import CKEditorWidget
    import warnings
    warnings.warn(
        DeprecationWarning('PHOTOLOGUE_USE_CKEDITOR setting will be removed in Photologue 2.9'))


class GalleryAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Gallery
        exclude = []


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'slug': ('title',)}
    form = GalleryAdminForm
    filter_horizontal = ["sites"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """ Set the current site as initial value. """
        if db_field.name == "sites":
            kwargs["initial"] = [Site.objects.get_current()]
        return super(GalleryAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """If the user has saved a gallery with a photo that belongs only to different Sites - 
        it might cause much confusion. So let them know."""
        obj.save()
        gallery_sites = set(obj.sites.all().values_list('id', flat=True))
        orphan_photos = []
        for photo in obj.photos.filter(is_public=True):
            photo_sites = set(photo.sites.all().values_list('id', flat=True))
            if photo_sites.isdisjoint(gallery_sites):
                orphan_photos.append(photo)
        if orphan_photos:
            msg = ungettext(
                'The following photo does not belong to the same site(s)'
                ' as the gallery, so will never be displayed: %(photo_list)s.',
                'The following photos do not belong to the same site(s)'
                ' as the gallery, so will never be displayed: %(photo_list)s.',
                len(orphan_photos)
            ) % {'photo_list': ", ".join([photo.title for photo in orphan_photos])}
            messages.warning(request, msg)


class GalleryUploadAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False  # To remove the 'Save and continue editing' button

    def save_model(self, request, obj, form, change):
        # Warning the user when things go wrong in a zip upload.
        obj.request = request
        obj.save()


class PhotoAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        caption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Photo
        exclude = []


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added',
                    'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    search_fields = ['title', 'slug', 'caption']
    list_per_page = 10
    prepopulated_fields = {'slug': ('title',)}
    form = PhotoAdminForm
    filter_horizontal = ["sites"]

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """ Set the current site as initial value. """
        if db_field.name == "sites":
            kwargs["initial"] = [Site.objects.get_current()]
        return super(PhotoAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)


class PhotoEffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color', 'brightness',
                    'contrast', 'sharpness', 'filters', 'admin_sample')
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


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)
