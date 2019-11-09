from PIL import Image, ImageDraw
import PIL
import os
import glob
import face_recognition
import cv2


class FaceDetector:
    def __init__(self):
        pass

    def scale_to_width(self, img, width):
        height = round(img.height * width / img.width)
        return img.resize((width, height), resample=PIL.Image.BILINEAR)

    def detect(self, img):
        cascade_path = "./haarcascade_frontalface_alt2.xml"
        list = []

        work_file_path = "./temp.jpg"

        resize_image = img
        if resize_image.width > 1024:
            resize_image = self.scale_to_width(resize_image, 1024)

        resize_image = resize_image.convert('RGB')
        resize_image.save(work_file_path, "JPEG")

        pil_image = Image.open(work_file_path)

        # OpenCVによる検出
        cascade = cv2.CascadeClassifier(cascade_path)
        opencv_image = cv2.imread(work_file_path, 0)
        cv_rects = cascade.detectMultiScale(
            opencv_image, scaleFactor=1.11, minNeighbors=2, minSize=(30, 30))

        # face recognitionによる検出
        face_reco_image = face_recognition.load_image_file(work_file_path)
        face_rects = face_recognition.face_locations(
            face_reco_image, number_of_times_to_upsample=0, model="cnn")

        # face recognitionの矩形処理
        if len(face_rects) > 0:
            for face_rect in face_rects:
                # 顔だけ切り出し
                top, right, bottom, left = face_rect
                width = right - left
                margin = int(width * 0.15)

                if pil_image.width < right + margin:
                    right = pil_image.width
                else:
                    right = right + margin

                if pil_image.height < bottom + margin:
                    bottom = pil_image.height
                else:
                    bottom = bottom + margin

                face_image = face_reco_image[top:bottom, left:right]
                dst = Image.fromarray(face_image)
                print(dst)
                list.append(dst)

        # face recognitionの矩形処理
        if len(face_rects) == 0 and len(cv_rects) > 0:
            for rect in cv_rects:
                # 顔だけ切り出し
                x = rect[0]
                y = rect[1]
                width = rect[2]
                height = rect[3]
                dst = pil_image[y:y + height, x:x + width]
                list.append(dst)

        return list
