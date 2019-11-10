# coding:utf-8
import unittest

from image_analyzer.ocr import OCR
import io
import os
import shutil
import urllib.request
from PIL import Image


class TestOCR(unittest.TestCase):

    def test_get_string(self):
        image_url = 'https://pbs.twimg.com/media/EH9AZ0iUcAIEv6I.jpg'
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)
        ocr = OCR()
        text = ocr.get_string(img)

        include_words = ['kusudaaina', '楠田亜衣奈']
        for word in include_words:
            if word in text:
                print("true!")

        print(text)


if __name__ == "__main__":
    unittest.main()
