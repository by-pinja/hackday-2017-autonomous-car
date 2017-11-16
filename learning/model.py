
import tensorflow as tf


class SteeringModel:

    def __init__(self, input):
        # output is
        input_layer = tf.layers.dense(
            inputs=input,
            units=120,
            activity_regularizer=tf.nn.sigmoid,
            name="input",
        )

        # Output is [x, y] (or perhaps [y, x])
        hidden = tf.layers.dense(
            inputs=input_layer,
            units=80,
            activity_regularizer=tf.nn.sigmoid,
            name="hidden"
        )

        hidden2 = tf.layers.dense(
            inputs=hidden,
            units=1,
            activity_regularizer=tf.nn.sigmoid,
            name="hidden2"
        )

        self._outputs = tf.layers.dense(
                inputs=tf.transpose(hidden2),
                units=2,
                activity_regularizer=tf.nn.sigmoid,
                name="output"
        )


    @property
    def output(self):
        return self._outputs
