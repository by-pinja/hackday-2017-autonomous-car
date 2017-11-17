
import tensorflow as tf


class SteeringModel:

    def __init__(self, input):
        # output is
        input_layer = tf.layers.dense(
            inputs=input,
            units=1024,
            activity_regularizer=tf.nn.sigmoid,
            name="input",
        )

        hidden = tf.layers.dense(
            inputs=input_layer,
            units=512,
            activity_regularizer=tf.nn.sigmoid,
            name="hidden",
        )

        hidden2 = tf.layers.dense(
            inputs=hidden,
            units=2,
            activity_regularizer=tf.nn.sigmoid,
            name="hidden2"
        )

        print("hidden2 shape {}".format(hidden2.shape))
        shaped = tf.reshape(hidden2, [1, 380])
        self._outputs = tf.layers.dense(
                inputs=shaped,
                units=2,
                activity_regularizer=tf.nn.sigmoid,
                name="output"
        )


    @property
    def output(self):
        return self._outputs
