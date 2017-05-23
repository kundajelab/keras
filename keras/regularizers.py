from __future__ import absolute_import
from . import backend as K
from .utils.generic_utils import get_from_module
import warnings


class Regularizer(object):

    def __call__(self, x):
        return 0

    def get_config(self):
        return {'name': self.__class__.__name__}

    def set_param(self, _):
        warnings.warn('The `set_param` method on regularizers is deprecated. '
                      'It no longer does anything, '
                      'and it will be removed after 06/2017.')

    def set_layer(self, _):
        warnings.warn('The `set_layer` method on regularizers is deprecated. '
                      'It no longer does anything, '
                      'and it will be removed after 06/2017.')



class SmoothnessRegularizer(Regularizer):

    def __init__(self, smoothness, l1=True, second_diff=False):
        self.smoothness = smoothness
        self.l1 = l1
        self.second_diff = second_diff

    def __call__(self, x):
        diff1 = x[1:, :]-x[:-1,:]
        diff2 = diff1[1:, :]-diff1[:-1,:]
        if self.second_diff == True:
            diff = diff2
        else:
            diff = diff1
        if self.l1 == True:
            return K.mean(K.abs(diff))*self.smoothness
        else:
            return K.mean(K.square(diff))*self.smoothness

    def get_config(self):
        return {'name': self.__class__.__name__,
                'smoothness': float(self.smoothness),
                'l1': bool(self.l1),
                'second_diff': bool(self.second_diff)}


class EigenvalueRegularizer(Regularizer):
    '''This takes a constant that controls
    the regularization by Eigenvalue Decay on the
    current layer and outputs the regularized
    loss (evaluated on the training data) and
    the original loss (evaluated on the
    validation data).
    '''
    def __init__(self, k):
        self.k = k

    def __call__(self, x):
        if K.ndim(x) != 2:
            raise ValueError('EigenvalueRegularizer '
                             'is only available for tensors of rank 2.')
        covariance = K.dot(K.transpose(x), x)
        dim1, dim2 = K.eval(K.shape(covariance))

        # Power method for approximating the dominant eigenvector:
        power = 9  # Number of iterations of the power method.
        o = K.ones([dim1, 1])  # Initial values for the dominant eigenvector.
        main_eigenvect = K.dot(covariance, o)
        for n in range(power - 1):
            main_eigenvect = K.dot(covariance, main_eigenvect)
        covariance_d = K.dot(covariance, main_eigenvect)

        # The corresponding dominant eigenvalue:
        main_eigenval = (K.dot(K.transpose(covariance_d), main_eigenvect) /
                         K.dot(K.transpose(main_eigenvect), main_eigenvect))
        # Multiply by the given regularization gain.
        regularization = (main_eigenval ** 0.5) * self.k
        return K.sum(regularization)


class L1L2Regularizer(Regularizer):

    def __init__(self, l1=0., l2=0.):
        self.l1 = K.cast_to_floatx(l1)
        self.l2 = K.cast_to_floatx(l2)

    def __call__(self, x):
        regularization = 0
        if self.l1:
            regularization += K.sum(self.l1 * K.abs(x))
        if self.l2:
            regularization += K.sum(self.l2 * K.square(x))
        return regularization

    def get_config(self):
        return {'name': self.__class__.__name__,
                'l1': float(self.l1),
                'l2': float(self.l2)}


# Aliases.

WeightRegularizer = L1L2Regularizer
ActivityRegularizer = L1L2Regularizer


def l1(l=0.01):
    return L1L2Regularizer(l1=l)


def l2(l=0.01):
    return L1L2Regularizer(l2=l)


def l1l2(l1=0.01, l2=0.01):
    return L1L2Regularizer(l1=l1, l2=l2)


def activity_l1(l=0.01):
    return L1L2Regularizer(l1=l)


def activity_l2(l=0.01):
    return L1L2Regularizer(l2=l)


def activity_l1l2(l1=0.01, l2=0.01):
    return L1L2Regularizer(l1=l1, l2=l2)


def get(identifier, kwargs=None):
    return get_from_module(identifier, globals(), 'regularizer',
                           instantiate=True, kwargs=kwargs)
