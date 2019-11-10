# coding:utf-8
from PIL import Image, ImageDraw
import PIL
import os
import glob
#import face_recognition
import cv2
import numpy as np
from math import ceil


class FaceDetector:
    def __init__(self):
        pass

    def scale_to_width(self, img, width):
        height = round(img.height * width / img.width)
        return img.resize((width, height), resample=PIL.Image.BILINEAR)

    def detect(self, img):

        if img.width > 1920:
             img = self.scale_to_width(img, 1920)

        img = img.convert('RGB')

        # OpenCV
        cv_list = self.opencv_detects(img)

        # face recognitionによる検出
        # CPUだけだと重すぎて無理なのでいったんコメントアウト
        #face_reco_image =  np.asarray(resize_image)
        # face_rects = face_recognition.face_locations(
        #    face_reco_image, number_of_times_to_upsample=0, model="cnn")
        face_rects = []
        list = []

        # face recognitionの矩形処理
        # if len(face_rects) > 0:
        #     for face_rect in face_rects:
        #         # 顔だけ切り出し
        #         top, right, bottom, left = face_rect
        #         width = right - left
        #         margin = int(width * 0.15)

        #         if pil_image.width < right + margin:
        #             right = pil_image.width
        #         else:
        #             right = right + margin

        #         if pil_image.height < bottom + margin:
        #             bottom = pil_image.height
        #         else:
        #             bottom = bottom + margin

        #         face_image = face_reco_image[top:bottom, left:right]
        #         dst = Image.fromarray(face_image)
        #         print(dst)
        #         list.append(dst)

        # face recognitionの矩形処理
        if len(face_rects) == 0 and len(cv_list) > 0:
            return cv_list

        return list

    def opencv_detects(self, img):
        cascade_path = "./haarcascade_frontalface_alt2.xml"
        cascade = cv2.CascadeClassifier(cascade_path)

        opencv_image = np.asarray(img)
        opencv_image = opencv_image[:, :, ::-1].copy()
        img_gray = cv2.cvtColor(opencv_image, cv2.COLOR_BGR2GRAY)
        org_width = opencv_image.shape[1]
        org_height = opencv_image.shape[0]

        list = []

        i = 0
        for j in range(-1, 2):
            # 拡大画像の作成
            big_img = np.zeros((org_height * 2, org_width * 2, 3), np.uint8)
            big_img[ceil(org_height/2.0):ceil(org_height/2.0*3.0),
                    ceil(org_width/2.0):ceil(org_width/2.0*3.0)] = opencv_image

            # 画像の中心位置
            center = tuple(
                np.array([big_img.shape[1] * 0.5, big_img.shape[0] * 0.5]))

            # 画像サイズの取得(横, 縦)
            size = tuple(np.array([big_img.shape[1], big_img.shape[0]]))

            # 回転させたい角度
            angle = 20 * float(j)
            # 拡大比率
            scale = 1.0

            # 回転変換行列の算出
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)

            # アフィン変換
            img_rot = cv2.warpAffine(
                big_img, rotation_matrix, size, flags=cv2.INTER_CUBIC)
            rot_gray = cv2.cvtColor(img_rot, cv2.COLOR_BGR2GRAY)

            # 顔判定
            faces = cascade.detectMultiScale(
                img_rot, scaleFactor=1.11, minNeighbors=3, minSize=(30, 30))
            # 顔があった場合
            if len(faces) > 0:
                for (x, y, w, h) in faces:
                    face = img_rot[y:y+h, x:x+w]
                    dst = Image.fromarray(face[:, :, ::-1].copy())
                    list.append(dst)

        return list
