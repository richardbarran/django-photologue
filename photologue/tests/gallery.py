from photologue.models import Gallery
from photologue.tests import helpers

class GalleryTest(helpers.PhotologueBaseTest):

    def setUp(self):
        """Create a test gallery with 2 photos."""
        super(GalleryTest, self).setUp()
        self.test_gallery = Gallery.objects.create(title='Fake Gallery', title_slug='fake-gallery')
        self.pl2 = helpers._create_new_photo(name='Landscape2', slug='landscape2')
        self.test_gallery.photos.add(self.pl)
        self.test_gallery.photos.add(self.pl2)

    def test_public(self):
        """Method 'public' should only return photos flagged as public."""
        self.assert_(self.test_gallery.public().count() == 2)
        self.pl.is_public = False
        self.pl.save()
        self.assert_(self.test_gallery.public().count() == 1)

    def test_photo_count(self):
        """Method 'photo_count' should return the count of the photos in this
        gallery."""
        self.assert_(self.test_gallery.photo_count() == 2)
        self.pl.is_public = False
        self.pl.save()
        self.assert_(self.test_gallery.photo_count() == 1)

        # Method takes an optional 'public' kwarg.
        self.assert_(self.test_gallery.photo_count(public=False) == 2)

    def test_sample(self):
        """Method 'sample' should return a random queryset of photos from the 
        gallery."""

        # By default we return all photos from the gallery (but ordered at random).
        self.assert_(len(self.test_gallery.sample()) == 2)

        # We can state how many photos we want.
        self.assert_(len(self.test_gallery.sample(count=1)) == 1)

        # If only one photo is public then the sample cannot have more than one
        # photo.
        self.pl.is_public = False
        self.pl.save()
        self.assert_(len(self.test_gallery.sample(count=2)) == 1)
