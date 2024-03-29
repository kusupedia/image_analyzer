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
        image_url = 'https://pbs.twimg.com/media/EHYzDHdUwAAFU2t.jpg'
        image_url = 'https://pbs.twimg.com/media/CDr7GM4UkAIB8lS.jpg'
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)
        faceDetector = FaceDetector()
        faces = faceDetector.detect(img)

        # 検証用に保管
        faceClassifier = FaceClassifier()
        i = 0
        for face in faces:
            face.save("./test_out/" + str(i) + ".jpg", "JPEG")
            predict_proba = faceClassifier.predict(face)
            if predict_proba < 0.10:
                print(predict_proba)
                print("kusuda!")
            else:
                print('other!')
            i += 1


if __name__ == "__main__":
    unittest.main()
