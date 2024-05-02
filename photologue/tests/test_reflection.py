
import sys
import os
sys.path.append(os.path.abspath('photologue/utils'))

import unittest
from PIL import Image
from watermark import reduce_opacity, apply_watermark

class TestWatermarkUtils(unittest.TestCase):

    def setUp(self):
        self.image = Image.new('RGB', (100, 100), color='white')
        self.watermark = Image.new('RGB', (20, 20), color='black')

    def test_reduce_opacity(self):
        opaque_image = reduce_opacity(self.image, 0.5)
        self.assertEqual(opaque_image.mode, 'RGBA')
        self.assertNotEqual(list(opaque_image.getdata()), list(self.image.getdata()))

    def test_apply_watermark(self):
        watermarked_image = apply_watermark(self.image, self.watermark, (10, 10))
        self.assertEqual(watermarked_image.mode, 'RGBA')
        self.assertNotEqual(list(watermarked_image.getdata()), list(self.image.getdata()))

    def test_apply_watermark_with_opacity(self):
        watermarked_image = apply_watermark(self.image, self.watermark, (10, 10), opacity=0.5)
        self.assertEqual(watermarked_image.mode, 'RGBA')
        self.assertNotEqual(list(watermarked_image.getdata()), list(self.image.getdata()))

    def test_apply_watermark_with_position(self):
        watermarked_image = apply_watermark(self.image, self.watermark, 'tile')
        self.assertEqual(watermarked_image.mode, 'RGBA')
        self.assertNotEqual(list(watermarked_image.getdata()), list(self.image.getdata()))

    def test_apply_watermark_with_scale(self):
        watermarked_image = apply_watermark(self.image, self.watermark, 'scale')
        self.assertEqual(watermarked_image.mode, 'RGBA')
        self.assertNotEqual(list(watermarked_image.getdata()), list(self.image.getdata()))

if __name__ == '__main__':
    unittest.main()