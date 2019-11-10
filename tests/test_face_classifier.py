# coding:utf-8
import unittest

from image_analyzer.face_classifier import FaceClassifier
from image_analyzer.face_detector import FaceDetector
import io
import os
import shutil
import urllib.request
from PIL import Image


class TestFaceClassifier(unittest.TestCase):

    def test_detect(self):
        shutil.rmtree('./test_out/')
        os.mkdir('./test_out')
        image_url = 'https://pbs.twimg.com/media/EHfTIHtU8AA1qQW.jpg'
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)
        faceDetector = FaceDetector()
        faces = faceDetector.detect(img)

        # 検証用に保管
        faceClassifier = FaceClassifier()
        i = 0
        for face in faces:
            face.save("./test_out/" + str(i) + ".jpg", "JPEG")
            predict_class = faceClassifier.predict(face)
            if predict_class == 0:
                print("true!")
            print('class:' + str(predict_class))
            i += 1


if __name__ == "__main__":
    unittest.main()
