import tensorflow as tf

import os

from learning import settings

from learning.model import SteeringModel

MODEL_DIR = "/home/joni/temp/cartest/test_model3/"

test_file = "/home/joni/temp/cartest/input/201711162110/frame_8.jpeg"


def _read_file_(image_file):
    image_string = tf.read_file(image_file)
    decoded = tf.image.decode_and_crop_jpeg(
        image_string,
        crop_window=settings.INPUT_CROP,
        channels=1
    )
    converted = tf.image.convert_image_dtype(decoded, dtype=settings.DATATYPE)
    # result = tf.reshape(converted, [settings.IMAGE_HEIGHT * settings.IMAGE_WIDTH * settings.IMAGE_CHANNELS])
    result = tf.squeeze(converted)
    result.set_shape([settings.IMAGE_HEIGHT, settings.IMAGE_WIDTH])

    return result


with tf.name_scope("Produce"):
    with tf.variable_scope("Model", reuse=None, initializer=None):
        produce_input = tf.placeholder(settings.DATATYPE, shape=settings.INPUT_SHAPE)
        produce_model = SteeringModel(produce_input)

pre_train_saver = tf.train.Saver(tf.trainable_variables())

with tf.Session() as session:
    meta_file = os.path.join(MODEL_DIR, "-50140")
    print("Opening file {}".format(meta_file))

    pre_train_saver.restore(session, meta_file)
    image = _read_file_(test_file)
    image_handle = session.run(image);
    result = session.run({'result': produce_model.output}, feed_dict={produce_input: image_handle})
    print(result)



