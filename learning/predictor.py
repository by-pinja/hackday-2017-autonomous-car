import tensorflow as tf

import os

from learning import settings
from learning.model import SteeringModel

class Predictor(object):
    def __init__(self, modelpath):
        with tf.name_scope("Produce"):
            with tf.variable_scope("Model", reuse=None, initializer=None):
                self.produce_input = tf.placeholder(settings.DATATYPE, shape=settings.INPUT_SHAPE)
                self.produce_model = SteeringModel(self.produce_input)

        pre_train_saver = tf.train.Saver(tf.trainable_variables())

        self.session = tf.Session()
        meta_file = os.path.join(modelpath, "-90201")
        print("Opening file {}".format(meta_file))
        pre_train_saver.restore(self.session, meta_file)

    # get image in tensorflow-suitable format
    def _read_file_(self, bytes):
        decoded = tf.image.decode_and_crop_jpeg(
            bytes,
            crop_window=settings.INPUT_CROP,
            channels=1
        )
        converted = tf.image.convert_image_dtype(decoded, dtype=settings.DATATYPE)
        # result = tf.reshape(converted, [settings.IMAGE_HEIGHT * settings.IMAGE_WIDTH * settings.IMAGE_CHANNELS])
        result = tf.squeeze(converted)
        result.set_shape([settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH])

        return result

    def read(self, bytes):
        image = self._read_file_(bytes)
        image_handle = self.session.run(image)
        return self.session.run({'result': self.produce_model.output}, feed_dict={self.produce_input: image_handle})

