# coding:utf-8
import pytesseract
import numpy as np
from PIL import Image


class OCR:
    def __init__(self):
        pass

    def get_string(self, img):
        text = pytesseract.image_to_string(img, lang='jpn')
        text = text.replace(' ', '')
        text = text.replace('\n', '')
        return text
