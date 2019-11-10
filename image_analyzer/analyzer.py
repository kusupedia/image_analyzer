# coding:utf-8
from image_analyzer.face_classifier import FaceClassifier
from image_analyzer.face_detector import FaceDetector
from image_analyzer.sqs_wrapper import SQSWrapper
from image_analyzer.ocr import OCR
import io
import urllib.request
from PIL import Image
import logging
from logging import config


class Analyzer:
    def __init__(self):
        config.fileConfig('conf/logging.conf', disable_existing_loggers=False)
        self.logger = logging.getLogger(__name__)

        self.sqs = SQSWrapper()
        self.faceDetector = FaceDetector()
        self.faceClassifier = FaceClassifier()
        self.ocr = OCR()
        self.logger.info('application initialize complete')

    def run(self):
        while True:
            tweets = self.sqs.fetch_tweet()
            self.logger.info('tweet count: %d', len(tweets))
            for tweet in tweets:
                self.analyze(tweet)

    def analyze(self, tweet):
        tweet_id = str(tweet['id'])
        image_urls = tweet['image_urls']
        for image_url in image_urls:
            if self.img_analyze(image_url, tweet_id) == True:
                # self.sqs.retweet(tweet_id)
                self.logger.info('tweet id: %s', str(tweet_id))
                break

    def img_analyze(self, image_url, tweet_id):
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)

        text = self.ocr.get_string(img)
        include_words = ['kusudaaina', '楠田亜衣奈']
        for word in include_words:
            if word in text:
                self.logger.info('text: %s', text)
                self.sqs.retweet(tweet_id)  # temporary insert
                return True

        faces = self.faceDetector.detect(img)
        max_match_rate = 0
        i = 0
        for face in faces:
            predict_proba = self.faceClassifier.predict(face)
            if predict_proba < 0.01:
                face.save("./save/" + str(tweet_id) +
                          "_" + str(i) + ".jpg", "JPEG")
                self.logger.info('url: %s proba: %s', image_url,
                                 str(predict_proba))
                return True
            i += 1
        return False
