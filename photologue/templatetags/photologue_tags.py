from django import template

register = template.Library()

@register.inclusion_tag('photologue/tags/next_in_gallery.html')
def next_in_gallery(photo, gallery):
    return {'photo': photo.get_next_in_gallery(gallery)}

@register.inclusion_tag('photologue/tags/prev_in_gallery.html')
def previous_in_gallery(photo, gallery):
    return {'photo': photo.get_previous_in_gallery(gallery)}
