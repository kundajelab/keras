from __future__ import absolute_import
import six
from . import backend as K
from .losses import mean_squared_error
from .losses import mean_absolute_error
from .losses import mean_absolute_percentage_error
from .losses import mean_squared_logarithmic_error
from .losses import hinge
from .losses import logcosh
from .losses import squared_hinge
from .losses import categorical_crossentropy
from .losses import sparse_categorical_crossentropy
from .losses import binary_crossentropy
from .losses import kullback_leibler_divergence
from .losses import poisson
from .losses import cosine_proximity
from .utils.generic_utils import deserialize_keras_object


def binary_accuracy(y_true, y_pred):
    return K.mean(K.equal(y_true, K.round(y_pred)), axis=-1)


def categorical_accuracy(y_true, y_pred):
    return K.cast(K.equal(K.argmax(y_true, axis=-1),
                          K.argmax(y_pred, axis=-1)),
                  K.floatx())


def sparse_categorical_accuracy(y_true, y_pred):
    return K.cast(K.equal(K.max(y_true, axis=-1),
                          K.cast(K.argmax(y_pred, axis=-1), K.floatx())),
                  K.floatx())


def top_k_categorical_accuracy(y_true, y_pred, k=5):
    return K.mean(K.in_top_k(y_pred, K.argmax(y_true, axis=-1), k), axis=-1)

def positive_accuracy(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,1.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    positive_accuracy=K.mean(K.equal(y_true_subset,K.round(y_pred_subset)))
    return positive_accuracy 


def negative_accuracy(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,0.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    negative_accuracy=K.mean(K.equal(y_true_subset,K.round(y_pred_subset)))
    return negative_accuracy 



def true_positives(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,1.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    positive_accuracy=K.sum(K.cast(K.equal(y_true_subset,K.round(y_pred_subset)),'int32'))
    return positive_accuracy 


def true_negatives(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,0.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    negative_accuracy=K.sum(K.cast(K.equal(y_true_subset,K.round(y_pred_subset)),'int32'))
    return negative_accuracy 


def false_positives(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,1.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    positive_accuracy=K.sum(K.cast(K.not_equal(y_true_subset,K.round(y_pred_subset)),'int32'))
    return positive_accuracy 


def false_negatives(y_true,y_pred):
    one_indices=K.cast(tf.where(K.equal(y_true,0.0)),'int32')
    y_true_subset=tf.gather_nd(y_true,one_indices)
    y_pred_subset=tf.gather_nd(y_pred,one_indices)
    negative_accuracy=K.sum(K.cast(K.not_equal(y_true_subset,K.round(y_pred_subset)),'int32'))
    return negative_accuracy 


# Aliases

mse = MSE = mean_squared_error
mae = MAE = mean_absolute_error
mape = MAPE = mean_absolute_percentage_error
msle = MSLE = mean_squared_logarithmic_error
cosine = cosine_proximity


def serialize(metric):
    return metric.__name__


def deserialize(name, custom_objects=None):
    return deserialize_keras_object(name,
                                    module_objects=globals(),
                                    custom_objects=custom_objects,
                                    printable_module_name='metric function')


def get(identifier):
    if isinstance(identifier, six.string_types):
        identifier = str(identifier)
        return deserialize(identifier)
    elif callable(identifier):
        return identifier
    else:
        raise ValueError('Could not interpret '
                         'metric function identifier:', identifier)
