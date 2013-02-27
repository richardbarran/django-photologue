# -*- coding: utf-8 -*-
from photologue.models import Image, PhotoEffect
from photologue.tests.helpers import PhotologueBaseTest

class PhotoEffectTest(PhotologueBaseTest):
    def test(self):
        effect = PhotoEffect(name='test')
        im = Image.open(self.pl.image.path)
        self.assert_(isinstance(effect.pre_process(im), Image.Image))
        self.assert_(isinstance(effect.post_process(im), Image.Image))
        self.assert_(isinstance(effect.process(im), Image.Image))

