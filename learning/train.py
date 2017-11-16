
from collections import namedtuple

import logging
import os
import pickle
import sys

import tensorflow as tf

import settings, reader
from model import SteeringModel
from util import get_model_init, load_model_config

logger = logging.getLogger(__name__)


ValidatedModel = namedtuple('ValidatedModel', ['model', 'cost'])


def save_model_config(model_config):
    config_file = os.path.join(settings.MODEL_SAVE_PATH, "model_config")
    with open(config_file, "wb") as outfile:
        settings_dict = {i: j for i, j in model_config.__class__.__dict__.items() if i[:2] != '__'}
        pickle.dump(settings_dict, outfile)


def get_validated_model(data, training_config, initializer, reuse=None):
    print("get_validated_model: {}".format(data))
    with tf.variable_scope("Model", reuse=reuse, initializer=initializer):
        model = SteeringModel(data[0])
        cost = get_cost(model, data[1], training_config)

    return ValidatedModel(model, cost)


def get_cost(model, targets, training_config):
    loss = tf.squared_difference(
        tf.cast(targets, settings.DATATYPE),
        model.output
    )
    cost = tf.reduce_sum(loss) / training_config.batch_size

    return cost


def train(model, cost, training_config):
    optimizer = tf.train.AdamOptimizer(training_config.learning_rate)
    tvars = tf.trainable_variables()
    gradients = tf.gradients(
        cost,
        tvars,
        # Experimental aggregation might reduce memory usage
        aggregation_method=tf.AggregationMethod.EXPERIMENTAL_TREE
    )
    clipped_grads, _ = tf.clip_by_global_norm(gradients, training_config.max_gradient)

    train_op = optimizer.apply_gradients(
        zip(clipped_grads, tvars),
        global_step=tf.train.get_or_create_global_step()
    )

    return train_op


def main(argv):
    if len(argv) > 2:
        model_path = argv[1]
        checkpoint = argv[2]
    else:
        model_path = None
        checkpoint = None


    training_config = settings.TrainingConfig()

    with tf.Graph().as_default() as graph:

        train_data = reader.get_dataset()
        train_data = train_data.shuffle(40)
        train_data = train_data.repeat(training_config.number_of_epochs)
        train_data_iterator = train_data.make_one_shot_iterator()
        train_data_input = train_data_iterator.get_next()

        # valid_data_iterator = valid_data.make_one_shot_iterator()

        initializer = tf.random_uniform_initializer(
            -training_config.init_scale,
            training_config.init_scale
        )

        with tf.name_scope("Train"):
            training_model = get_validated_model(
                train_data_input,
                training_config,
                initializer,
                reuse=None
            )
            tf.summary.scalar("Training_Loss", training_model.cost)
            training_op = train(training_model, training_model.cost, training_config)

        """
        with tf.name_scope("Valid"):
            validation_model = get_validated_model(
                valid_data_iterator.get_next(),
                model_config,
                training_config,
                initializer,
                reuse=True
            )
            tf.summary.scalar("Validation_Loss", validation_model.cost)
        """

        with tf.name_scope("SteeringModel"):
            with tf.variable_scope("Model", reuse=tf.AUTO_REUSE, initializer=initializer):
                produce_input = tf.placeholder(settings.DATATYPE, shape=settings.INPUT_SHAPE)
                produce_model = SteeringModel(produce_input)

        sv = tf.train.Supervisor(logdir=settings.LOG_PATH, init_fn=get_model_init(model_path, checkpoint))
        with sv.managed_session() as session:
            cost = 0
            steps = 0
            try:
                while True:
                    # session.run(training_op)
                    fetches = {
                        'training_op': training_op,
                        'cost': training_model.cost,
                        'result': training_model.model.output,
                    }
                    result = session.run(fetches)
                    steps += 1
                    cost += result['cost']

                    if steps % 1000 == 0:
                        print("Step {}: Cost {}, latest command {}".format(steps, cost / steps, result['result']))
            except KeyboardInterrupt:
                print("Interrupted")

            sv.saver.save(session, settings.MODEL_SAVE_PATH, global_step=sv.global_step)


if __name__ == "__main__":
    if not os.path.exists(settings.LOG_PATH):
        os.makedirs(settings.LOG_PATH)
    if not os.path.exists(settings.MODEL_SAVE_PATH):
        os.makedirs(settings.MODEL_SAVE_PATH)

    logger.setLevel(logging.DEBUG)
    con = logging.StreamHandler()
    con.setLevel(logging.DEBUG)
    logger.addHandler(con)
    f = logging.FileHandler(filename=os.path.join(settings.LOG_PATH, 'output.log'))
    f.setLevel(logging.DEBUG)
    logger.addHandler(f)
    tf.app.run(argv=sys.argv)
