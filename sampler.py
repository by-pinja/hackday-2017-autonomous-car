import time
import datetime
import os
import shutil
import csv
from camera import CameraModule


class Sampler(object):
    STORAGE_ROOT = '/home/pi/'
    CAPTURE_INTERVAL_SECS = 1.0

    def __init__(self):
        self.frame = 0
        self.sequence = None
        self.last_capture = None
        self.sequence_path = None
        self.steering_file_path = None
        self.camera_module = CameraModule()
        self.csv_rows = []

    def start(self):
	self.csv_rows = []
        self.frame = 0
        self.sequence = time.strftime("%Y%m%d%H%M")
        self.sequence_path = os.path.join(self.STORAGE_ROOT, self.sequence)
        if not os.path.exists(self.sequence_path):
            os.makedirs(self.sequence_path)
        self.steering_file_path = os.path.join(self.sequence_path, 'steering.csv')
        self.last_capture = None

    def reject(self):
        shutil.rmtree(self.sequence_path, ignore_errors=True)

    def capture(self, steering, propagation):
        print("capture")
        now = datetime.datetime.now()
        if self.last_capture is not None and (now - self.last_capture).total_seconds() < self.CAPTURE_INTERVAL_SECS:
            print("skipping capture")
            return
        self.last_capture = now
        self.frame += 1
        image = self.camera_module.capture()
        filepath = os.path.join(self.sequence_path, "frame_{}.jpeg".format(self.frame))
        print("Saving file {}".format(datetime.datetime.now()))
        image.save(filepath)
        print("Save complete {}".format(datetime.datetime.now()))
        self.csv_rows.append([self.frame, propagation, steering])
        
    def save_run(self):
        print('saving steering data to csv {}'.format(datetime.datetime.now()))
        with open(self.steering_file_path, 'w') as csvfile:
            writer = csv.writer(csvfile, delimiter=';')
            for csv_row in self.csv_rows:
                writer.writerow(csv_row)
        print("saved steering data {}".format(datetime.datetime.now()))
