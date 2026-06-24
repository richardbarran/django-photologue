from ..models import Image, PhotoEffect
from .helpers import PhotologueBaseTest


class PhotoEffectTest(PhotologueBaseTest):

    def test(self):
        effect = PhotoEffect(name='test')
        with self.pl.image.storage.open(self.pl.image.name) as file:
            with Image.open(file) as im:
                self.assertIsInstance(effect.pre_process(im), Image.Image)
                self.assertIsInstance(effect.post_process(im), Image.Image)
                self.assertIsInstance(effect.process(im), Image.Image)
