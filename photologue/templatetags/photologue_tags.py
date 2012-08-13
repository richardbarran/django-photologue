from django import template
from django.db.models import get_model

import random

register = template.Library()

Gallery = get_model('photologue', 'Gallery')
Photo = get_model('photologue', 'Photo')

@register.inclusion_tag('photologue/tags/next_in_gallery.html')
def next_in_gallery(photo, gallery):
    return {'photo': photo.get_next_in_gallery(gallery)}

@register.inclusion_tag('photologue/tags/prev_in_gallery.html')
def previous_in_gallery(photo, gallery):
    return {'photo': photo.get_previous_in_gallery(gallery)}

@register.simple_tag
def cycle_lite_gallery(gallery_title, height, width):
    """Generate image tags for jquery slideshow gallery.
    See http://malsup.com/jquery/cycle/lite/"""
    html = ""
    first = 'class="first"'
    for p in Gallery.objects.get(title=gallery_title).public():
        html += u'<img src="%s" alt="%s" height="%s" width="%s" %s />' % (p.get_display_url(), p.title, height, width, first)
        first = None
    return html

@register.tag
def get_photo(parser, token):
    """Get a single photo from the photologue library and return the img tag to display it.

    Takes 3 args:
    - the photo to display. This can be either the slug of a photo, or a variable that holds either a photo instance or a integer (photo id)
    - the photosize to use.
    - a CSS class to apply to the img tag.
    """
    try:
        tag_name, photo, photosize, css_class = token.split_contents() # Split the contents of the tag, i.e. tag name + argument.
    except ValueError:
        msg = '%r tag requires 3 arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return PhotoNode(photo, photosize[1:-1], css_class[1:-1])

class PhotoNode(template.Node):

    def __init__(self, photo, photosize, css_class):
        self.photo = photo
        self.photosize = photosize
        self.css_class = css_class

    def render(self, context):
        try:
            a = template.resolve_variable(self.photo, context)
        except:
            a = self.photo
        if isinstance(a, Photo):
            p = a
        else:
            try:
                p = Photo.objects.get(title_slug=a)
            except Photo.DoesNotExist:
                # Ooops. Fail silently
                return None
        if not p.is_public:
            return None
        func = getattr(p, 'get_%s_url' % (self.photosize), None)
        if func is None:
            return 'A "%s" photo size has not been defined.' % (self.photosize)
        else:
            return u'<img class="%s" src="%s" alt="%s" />' % (self.css_class, func(), p.title)

@register.tag
def get_rotating_photo(parser, token):
    """Pick at random a photo from a given photologue gallery and return the img tag to display it.

    Takes 3 args:
    - the gallery to pick a photo from. This can be either the slug of a gallery, or a variable that holds either a gallery instance or a gallery slug.
    - the photosize to use.
    - a CSS class to apply to the img tag.
    """
    try:
        tag_name, gallery, photosize, css_class = token.split_contents() # Split the contents of the tag, i.e. tag name + argument.
    except ValueError:
        msg = '%r tag requires 3 arguments' % token.contents[0]
        raise template.TemplateSyntaxError(msg)
    return PhotoGalleryNode(gallery, photosize[1:-1], css_class[1:-1])

class PhotoGalleryNode(template.Node):

    def __init__(self, gallery, photosize, css_class):
        self.gallery = gallery
        self.photosize = photosize
        self.css_class = css_class

    def render(self, context):
        try:
            a = template.resolve_variable(self.gallery, context)
        except:
            a = self.gallery
        if isinstance(a, Gallery):
            g = a
        else:
            try:
                g = Gallery.objects.get(title_slug=a)
            except Gallery.DoesNotExist:
                return None
        photos = g.public()
        if len(photos) > 1:
            r = random.randint(0, len(photos) - 1)
            p = photos[r]
        elif len(photos) == 1:
            p = photos[0]
        else:
            return None
        func = getattr(p, 'get_%s_url' % (self.photosize), None)
        if func is None:
            return 'A "%s" photo size has not been defined.' % (self.photosize)
        else:
            return u'<img class="%s" src="%s" alt="%s" />' % (self.css_class, func(), p.title)
