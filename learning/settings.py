import tensorflow as tf

INPUT_DATA_DIR = "/home/joni/temp/cartest/input/201711162007/"
LOG_PATH = "/home/joni/temp/cartest/output/"
MODEL_SAVE_PATH = "/home/joni/temp/cartest/model/"

IMAGE_WIDTH = 320
IMAGE_HEIGHT = 190
IMAGE_CHANNELS = 1
INPUT_CROP = [50, 0, IMAGE_HEIGHT, IMAGE_WIDTH]
INPUT_SHAPE = [IMAGE_HEIGHT, IMAGE_WIDTH]

# Ratio of input data reserved for validation
VALIDATION_RATIO = 0.25

DATATYPE = tf.float32


class TrainingConfig:
    init_scale = 0.05

    batch_size = 15

    # Doesn't matter much in practice, model is just trained as long as it takes
    number_of_epochs = 10000

    # http://proceedings.mlr.press/v28/pascanu13.pdf suggests 0.5 - 10 times average norm
    max_gradient = 10.0  # http://torch.ch/blog/2016/07/25/nce.html
    learning_rate = 1e-4
