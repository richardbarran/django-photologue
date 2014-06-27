from ..models import Image, PhotoEffect
from .helpers import PhotologueBaseTest


class PhotoEffectTest(PhotologueBaseTest):

    def test(self):
        effect = PhotoEffect(name='test')
        im = Image.open(self.pl.image.storage.open(self.pl.image.name))
        self.assertIsInstance(effect.pre_process(im), Image.Image)
        self.assertIsInstance(effect.post_process(im), Image.Image)
        self.assertIsInstance(effect.process(im), Image.Image)
