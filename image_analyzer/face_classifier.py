# coding:utf-8
from tensorflow import keras
import cv2
import numpy as np
from PIL import Image

IMG_SIZE = 150


class FaceClassifier:
    def __init__(self):
        self.model = keras.models.load_model('/usr/local/model/model.h5')
        print(self.model.summary())

    def predict(self, img):
        img = img.convert("RGB").resize(
            (IMG_SIZE, IMG_SIZE), Image.ANTIALIAS)
        img = np.asarray(img, dtype=np.float32).reshape(
            IMG_SIZE, IMG_SIZE, 3)
        img /= 255.0
        predict_classes = self. model.predict_classes(np.array([img]), 1)
        predict_proba = self. model.predict_proba(np.array([img]), 1)
        return predict_classes[0], predict_proba[0]
