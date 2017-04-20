'machine leaning'
import abc
import copy
import numpy as np
import pdb
import unittest


class Model(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def predict(self, w, x):
        'return np.array'
        pass

    @abc.abstractmethod
    def gradient_prediction_wrt_features(self, features, prediction, weights):
        'return np.array'
        pass

    @abc.abstractmethod
    def gradient_prediction_wrt_weights(self, features, prediction, weights):
        'return np.array'
        pass

    @abc.abstractmethod
    def n_weights(self):
        'return length of w vector: Number'
        pass


class Criterion(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loss(self, prediction, target):
        'return Number'
        pass

    @abc.abstractmethod
    def derivative_loss_wrt_prediction(self, loss, prediction, target):
        'return np.array'
        pass

    @abc.abstractmethod
    def derivative_loss_wrt_target(self, loss, prediction, target):
        'return np.array'
        pass


class ModelCriterion(object):
    def __init__(self, model=None, criterion=None):
        assert isinstance(model, machine_learning.Model)
        assert isinstance(criterion, machine_learning.Criterion)
        self.model = model
        self.criterion = criterion

    def loss_prediction(self, features, target, weights):
        prediction = self.model.predict(features, weights)
        loss = self.criterion.loss(prediction, target)
        return loss, predictiont

    def gradient_wrt_weights(self, features, loss, prediction, target, weights):
        'using the chain rule'
        gradient_prediction_wrt_weights = self.model.gradient_prediction_wrt_weights(features, prediction, weights)
        derivate_loss_wrt_prediction = self.criterion.derivative_loss_wrt_prediction(loss, prediction, target)
        result = gradient_prediction_wrt_weights * derivate_loss_wrt_prediction
        return result


class Linear(Model):
    'y = bias + coef * x'
    def __init__(self, n_inputs):
        self.n_inputs = n_inputs

    def predict(self, features, weights):
        # bias = w[0]
        # coef = w[1:]
        assert len(features) == self.n_inputs
        assert len(weights) == self.n_inputs + 1

        result_scalar = weights[0] + np.dot(features, weights[1:])
        result = np.array((result_scalar,))
        return result

    def gradient_prediction_wrt_weights(self, features, prediction, weights):
        assert len(features) == self.n_inputs
        assert len(prediction) == 1
        assert len(weights) == self.n_inputs + 1

        result = np.empty(self.n_inputs + 1)
        result[0] = 1
        result[1:] = copy.copy(features)
        return result

    def gradient_prediction_wrt_features(self, features, prediction, weights):
        assert len(prediction) == 1
        assert len(features) == self.n_inputs
        assert len(weights) == self.n_inputs + 1

        result = copy.copy(weights[1:])
        return result

    def n_weights(self):
        return self.n_inputs + 1


class UnittestLinear(unittest.TestCase):
    def setUp(self):
        self.w = np.array((-7, 3, 6))

    def test_construction_nweights(self):
        tests = (
            0,
            1,
            2,
        )
        for test in tests:
            model = Linear(test)
            self.assertTrue(isinstance(model, Linear))
            self.assertEqual(test + 1, model.n_weights())

    def test_predict(self):
        weights = np.array((1, 2, 3))
        tests = (
            (0, np.empty((0)), 1),
            (1, np.array((1,)), 3),
            (2, np.array((1, 2)), 9),
        )
        for test in tests:
            n_inputs, features, prediction_expected = test
            model = Linear(n_inputs)
            weights_test = weights[:model.n_weights()]
            prediction_actual = model.predict(features, weights_test)
            self.assertEqual(prediction_expected, prediction_actual)
            self.assertTrue(isinstance(prediction_actual, np.ndarray))

    def test_gradient_prediction_wrt_weights(self):
        weights = np.array((10, 20, 30))
        tests = (
            (0, np.empty((0)), np.array((1))),
            (1, np.array((1,)), np.array((1, 1))),
            (2, np.array((1, 2)), np.array((1, 1, 2))),
        )
        for test in tests:
            n_inputs, features, gradient_expected = test
            model = Linear(n_inputs)
            weights_test = weights[:model.n_weights()]
            prediction_actual = model.predict(features, weights_test)
            gradient_actual = model.gradient_prediction_wrt_weights(features, prediction_actual, weights_test)
            self.assertTrue((gradient_expected == gradient_actual).all())

    def test_gradient_prediction_wrt_features(self):
        weights = np.array((1, 2, 3))
        tests = (
            # (0, np.empty((0)), np.empty((0))),
            (1, np.array((1,)), np.array((2,))),
            (2, np.array((1, 2)), np.array((2, 3))),
        )
        for test in tests:
            n_inputs, features, gradient_expected = test
            model = Linear(n_inputs)
            weights_test = weights[:model.n_weights()]
            prediction_actual = model.predict(features, weights_test)
            gradient_actual = model.gradient_prediction_wrt_features(features, prediction_actual, weights_test)
            self.assertTrue((gradient_expected == gradient_actual).all())


class SquaredLoss(Criterion):
    def __init__(self):
        pass

    def loss(self, prediction, target):
        difference = prediction - target
        result = difference * difference
        return result

    def derivative_loss_wrt_prediction(self, loss, prediction, target):
        return 2.0 * (prediction - target)

    def derivative_loss_wrt_target(self, loss, prediction, target):
        return - 2.0 * (prediction - target)


class TestSquaredLoss(unittest.TestCase):
    def test_construction(self):
        criterion = SquaredLoss()
        self.assertTrue(isinstance(criterion, SquaredLoss))

    def test_loss(self):
        tests = (
            (10, 12, 4),
            (12, 10, 4),
            (10, 10, 0),
        )
        for test in tests:
            prediction, target, loss_expected = test
            criterion = SquaredLoss()
            loss_actual = criterion.loss(prediction, target)
            self.assertEqual(loss_expected, loss_actual)

    def test_derivative_loss_wrt_prediction(self):
        tests = (
            (4, 10, 12, -4),
            (9, 10, 13, -6),
        )
        for test in tests:
            loss, prediction, target, derivative_expected = test
            criterion = SquaredLoss()
            derivative_actual = criterion.derivative_loss_wrt_prediction(loss, prediction, target)
            self.assertEqual(derivative_expected, derivative_actual)

    def test_derivative_loss_wrt_target(self):
        tests = (
            (4, 10, 12, 4),
            (9, 10, 13, 6),
        )
        for test in tests:
            loss, prediction, target, derivative_expected = test
            criterion = SquaredLoss()
            derivative_actual = criterion.derivative_loss_wrt_target(loss, prediction, target)
            self.assertEqual(derivative_expected, derivative_actual)


if __name__ == '__main__':
    unittest.main()
    if False:
        pdb
