import unittest
from image_analyzer.face_detector import FaceDetector
import io
import urllib.request
from PIL import Image


class TestFaceDetector:

    def test_detect(self):
        image_url = 'https://pbs.twimg.com/media/EHfTIHtU8AA1qQW.jpg'
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)
        faceDetector = FaceDetector()
        faces = faceDetector.detect(img)
        for face in faces:
            face.save("../test_out", "JPEG")


if __name__ == "__main__":
    unittest.main()
