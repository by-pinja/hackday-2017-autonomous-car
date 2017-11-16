import time
import datetime
import os
import shutil
import csv
from .camera import CameraModule


class App(object):
    STORAGE_ROOT = '~'
    CAPTURE_INTERVAL_SECS = 0.5

    def __init__(self):
        self.frame = 0
        self.sequence = None
        self.last_capture = None
        self.camera_module = CameraModule()

    def start(self):
        self.frame = 1
        self.sequence = time.strftime("%Y%m%d%H%M")
        self.sequence_path = os.path.join(self.STORAGE_ROOT, self.sequence)
        if not os.path.exists(self.sequence_path):
            os.makedirs(self.sequence_path)
        self.steering_file_path = os.path.join(self.sequence_path, 'steering.csv')
        self.last_capture = None

    def stop(self):
        pass

    def reject(self):
        self.stop()
        shutil.rmtree(self.sequence_path, ignore_errors=True)

    def capture(self, gas, steering):
        now = datetime.datetime.now()
        if self.last_capture is None or (now - self.last_capture).total_seconds() < self.CAPTURE_INTERVAL_SECS:
            return
        self.last_capture = now
        self.frame += 1
        image = self.camera_module.capture()
        image.save(os.path.join(self.sequence_path, "frame_{}".format(self.frame)))
        with open(self.steering_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            writer.writerow([self.frame, gas, steering])
