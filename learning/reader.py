
from collections import namedtuple

import logging
import os

import tensorflow as tf

import settings

logger = logging.getLogger(__name__)

Input = namedtuple('Input', ['data', 'labels', 'epoch_size'])


def _read_image_(image_file):
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


def _map_line_(line):
    decoded = tf.decode_csv(line, record_defaults=((1,), (0.0,), (0.0,)), field_delim=';')
    return decoded[1], decoded[2]


def _read_label_file(labelfile):
    return tf.data.TextLineDataset(labelfile).map(_map_line_)


def get_dataset():

    data_dir = settings.INPUT_DATA_DIR
    data_directories = sorted(os.listdir(data_dir))
    print("Data directories {}".format(data_directories))

    image_files = []
    csv_files = []
    for directory in data_directories:
        dir = os.path.join(data_dir, directory)
        print("Data directory {}".format(dir))
        file_names = [os.path.join(dir, i) for i in os.listdir(dir) if i.endswith('.jpeg')]
        sorted_files = sorted(file_names)
        image_files += sorted_files
        csv_files.append(os.path.join(dir, 'steering.csv'))

    print("Got {} image files".format(len(image_files)))

    image_files = tf.constant(image_files)
    image_dataset = tf.data.Dataset.from_tensor_slices(image_files)
    image_dataset = image_dataset.map(lambda image_file: _read_image_(image_file))

    csv_files = tf.constant(csv_files)
    label_dataset = tf.data.Dataset.from_tensor_slices(csv_files)
    label_dataset = label_dataset.flat_map(lambda filename:_read_label_file(filename))

    return tf.data.Dataset.zip((image_dataset, label_dataset))


