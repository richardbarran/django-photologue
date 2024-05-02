import unittest
from PIL import Image
import sys
import os
sys.path.append(os.path.abspath('photologue/utils'))
from watermark import reduce_opacity, apply_watermark

class TestWatermark(unittest.TestCase):

    def setUp(self):
        self.image = Image.new('RGB', (100, 100), color='white')
        self.mark = Image.new('RGB', (20, 20), color='black')

    def test_reduce_opacity(self):
        reduced_opacity_image = reduce_opacity(self.mark, 0.5)
        self.assertEqual(reduced_opacity_image.mode, 'RGBA')

    def test_apply_watermark(self):
        watermarked_image = apply_watermark(self.image, self.mark, (10, 10))
        self.assertEqual(watermarked_image.size, self.image.size)

    def test_apply_watermark_with_opacity(self):
        watermarked_image = apply_watermark(self.image, self.mark, (10, 10), opacity=0.5)
        self.assertEqual(watermarked_image.size, self.image.size)

    def test_apply_watermark_with_tile_position(self):
        watermarked_image = apply_watermark(self.image, self.mark, 'tile')
        self.assertEqual(watermarked_image.size, self.image.size)

    def test_apply_watermark_with_scale_position(self):
        watermarked_image = apply_watermark(self.image, self.mark, 'scale')
        self.assertEqual(watermarked_image.size, self.image.size)

    def test_apply_watermark_with_invalid_position(self):
        with self.assertRaises(TypeError):
            apply_watermark(self.image, self.mark, 'invalid')

if __name__ == '__main__':
    unittest.main()