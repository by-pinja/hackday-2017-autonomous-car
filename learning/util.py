import os
import pickle

import tensorflow as tf


def load_model_config(model_path):
    config_file = os.path.join(model_path, 'model_config')
    with open(config_file, 'rb') as infile:
        conf_dict = pickle.load(infile)
        # For backwards compatibility
        if 'input_dtype' not in conf_dict:
            conf_dict['input_dtype'] = tf.int32
        class Config:
            pass
        result = Config()
        result.__dict__ = conf_dict
        return result


def get_model_init(model_path, checkpoint):
    if model_path and checkpoint:
        pre_train_saver = tf.train.Saver(tf.trainable_variables())

        def load_pretrain(sess):
            pre_train_saver.restore(
                sess,
                os.path.join(model_path, checkpoint)
            )

        return load_pretrain
    return None
