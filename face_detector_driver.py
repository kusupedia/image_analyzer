import unittest
from image_analyzer.face_detector import FaceDetector
import io
import urllib.request
from PIL import Image

image_url = 'https://pbs.twimg.com/media/EHfTIHtU8AA1qQW.jpg'
f = io.BytesIO(urllib.request.urlopen(image_url).read())
img = Image.open(f)
faceDetector = FaceDetector()
faces = faceDetector.detect(img)
i = 0
for face in faces:
    face.save("./test_out/" + str(i) + ".jpg", "JPEG")
    i += 1
