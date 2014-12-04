from django.core.exceptions import ValidationError

from .factories import PhotoSizeFactory
from .helpers import PhotologueBaseTest


class PhotoSizeNameTest(PhotologueBaseTest):

    def test_valid_name(self):
        """We are restricted in what names we can enter."""

        photosize = PhotoSizeFactory()
        photosize.name = None
        with self.assertRaisesMessage(ValidationError, 'This field cannot be null.'):
            photosize.full_clean()

        photosize = PhotoSizeFactory(name='')
        with self.assertRaisesMessage(ValidationError, 'This field cannot be blank.'):
            photosize.full_clean()

        for name in ('a space', 'UPPERCASE', 'bad?chars'):
            photosize = PhotoSizeFactory(name=name)
            with self.assertRaisesMessage(ValidationError,
                                          'Use only plain lowercase letters (ASCII), numbers and underscores.'):
                photosize.full_clean()

        for name in ('label', '2_words'):
            photosize = PhotoSizeFactory(name=name)
            photosize.full_clean()
