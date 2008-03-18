import getopt, sys

try:
    import settings # Assumed to be in the same directory.
    from django.core.management import setup_environ
except ImportError:
    import sys
    sys.stderr.write("Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
    sys.exit(1)


def precache(sizes=[], reset=False):
    # setup django environment
    setup_environ(settings)

    # import models
    from photologue.models import Photo, PhotoSize, PhotoSizeCache

    cache = PhotoSizeCache()

    print 'Caching photos, this may take a while...'

    for photo in Photo.objects.all():
        if len(sizes):
            for size in sizes:
                photosize = cache.sizes.get(size, None)
                if photosize is None:
                    print '\nA photosize named "%s" was not found...' % size
                else:
                    if reset:
                        photo.remove_size(photosize)
                    photo.create_size(photosize)
        else:
            for size in caches.sizes.values():
                if reset:
                    Photo.remove_size(photosize)
                photo.create_size(photosize)

    print ' Complete.'
    sys.exit(2)


def reset():
    # setup django environment
    setup_environ(settings)

    # import models
    from photologue.models import Photo, PhotoSize

    print 'Reseting photo cache, this may take a while...'

    for photo in Photo.objects.all():
        photo.clear_cache()

    print ' Complete.'
    sys.exit(2)


def usage():
    print """

pl-admin.py - Photologue administration script.

Available Commands:
 pl-admin.py create Resizes and caches all defined photo sizes for each image.
 pl-admin.py reset  Removes all cached images.

Options:
 --reset (-r) If calling create the script will clear the existing photo cache
              before regenerating the specified size (or sizes)
 --size (-s)  The name of a photosize generate

Usage:
 pl-admin.py [options] command

Examples:
 pl-admin.py -r -s=thumbnail create
 pl-admin.py -s=thumbnail -s=display create
 pl-admin.py reset

"""

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hrs:",
                                   ["help", "reset", "sizes="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    r = False
    s = []
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit(2)
        if o in ("-r", "--reset"):
            r = True
        elif o in ("-s", "--sizes"):
            s.append(a.strip('='))
        else:
            usage()
            sys.exit(2)

    if len(args) == 1:
        command = args[0]
        if command == 'create':
            precache(s, r)
        elif command == 'reset':
            reset()

    usage()


if __name__ == '__main__':
    main()
