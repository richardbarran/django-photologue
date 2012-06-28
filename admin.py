from photologue.models import Photo, GalleryUpload
from albums.models import myPhoto, myGalleryUpload
from django.contrib import admin
from django import forms
from adminsortable.admin import SortableAdmin


class myPhotoAdmin(SortableAdmin):
    list_display = ('id', 'title', 'caption', 'tags', 'is_public', 'admin_thumbnail')
    list_editable = ('title', 'caption', 'tags')
    list_filter = ('tags', 'galleries')
    search_fields = ( 'title', 'caption', 'tags')

    def formfield_for_dbfield(self, db_field, **kwargs):
        formfield = super(myPhotoAdmin, self).formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == 'caption':
            formfield.widget = forms.Textarea(attrs={'cols': 60, 'rows': 2})
        return formfield

admin.site.unregister(Photo)
admin.site.register(myPhoto, myPhotoAdmin)

admin.site.unregister(GalleryUpload)
admin.site.register(myGalleryUpload)