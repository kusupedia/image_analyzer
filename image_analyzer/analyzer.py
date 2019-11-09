from image_analyzer.face_classifier import FaceClassifier
from image_analyzer.face_detector import FaceDetector
from image_analyzer.sqs_wrapper import SQSWrapper
import io
import urllib.request
from PIL import Image


class Analyzer:
    def __init__(self):
        self.sqs = SQSWrapper()

    def run(self):
        while True:
            tweets = self.sqs.fetch_tweet()
            for tweet in tweets:
                self.analyze(tweet)

    def analyze(self, tweet):
        tweet_id = str(tweet['id'])
        image_urls = tweet['image_urls']
        for image_url in image_urls:
            if self.img_analyze(image_url) == True:
                # self.sqs.retweet(tweet_id)
                break

    def img_analyze(self, image_url):
        f = io.BytesIO(urllib.request.urlopen(image_url).read())
        img = Image.open(f)

        faceDetector = FaceDetector()
        faceClassifier = FaceClassifier()

        faces = faceDetector.detect(img)
        max_match_rate = faceClassifier.classificate(faces)

        if max_match_rate > 95:
            return True
        return False
