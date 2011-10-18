# Required PIL classes may or may not be available from the root namespace
# depending on the installation method used.
try:
    import Image
except ImportError:
    try:
        from PIL import Image
    except ImportError:
        raise ImportError('Photologue was unable to import the Python Imaging Library. Please confirm it`s installed and available on your current Python path.')


def is_transparent(image):
    """
    Check to see if an image is transparent.
    """
    if not isinstance(image, Image.Image):
        # Can only deal with PIL images, fall back to the assumption that that
        # it's not transparent.
        return False
    return (image.mode in ('RGBA', 'LA') or
            (image.mode == 'P' and 'transparency' in image.info))


def colorspace(im, bw=False, replace_alpha=False, **kwargs):
    """
    Convert images to the correct color space.

    A passive option (i.e. always processed) of this method is that all images
    (unless grayscale) are converted to RGB colorspace.

    This processor should be listed before :func:`scale_and_crop` so palette is
    changed before the image is resized.

    bw
        Make the thumbnail grayscale (not really just black & white).

    replace_alpha
        Replace any transparency layer with a solid color. For example,
        ``replace_alpha='#fff'`` would replace the transparency layer with
        white.

    """
    transparent = is_transparent(im)
    if bw:
        if im.mode in ('L', 'LA'):
            return im
        if is_transparent:
            return im.convert('LA')
        else:
            return im.convert('L')
    if im.mode in ('L', 'RGB'):
        return im
    if transparent:
        if im.mode != 'RGBA':
            im = im.convert('RGBA')
        if not replace_alpha:
            return im
        base = Image.new('RGBA', im.size, replace_alpha)
        base.paste(im)
        im = base
    return im.convert('RGB')
