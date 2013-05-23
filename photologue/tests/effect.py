# -*- coding: utf-8 -*-
from photologue.models import Image, PhotoEffect
from photologue.tests.helpers import PhotologueBaseTest

class PhotoEffectTest(PhotologueBaseTest):
    def test(self):
        effect = PhotoEffect(name='test')
        im = Image.open(self.pl.image.path)
        self.assertIsInstance(effect.pre_process(im), Image.Image)
        self.assertIsInstance(effect.post_process(im), Image.Image)
        self.assertIsInstance(effect.process(im), Image.Image)

