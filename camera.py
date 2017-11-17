from io import BytesIO
from time import sleep
from picamera import PiCamera
from PIL import Image


class CameraModule:

    def __init__(self, *args, **kwargs):
        self.camera = PiCamera(resolution=(320, 240))
        sleep(2)

    def capture(self):
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        return Image.open(stream)

    def capture_image_string(self):
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        return stream.getvalue()
