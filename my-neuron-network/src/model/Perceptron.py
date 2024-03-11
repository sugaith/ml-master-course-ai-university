import random
import numpy as np


def sigmoid(new_input: np.float32) -> np.float32:
    # normalizes the input returning a float between 0 and 1
    return 1 / (1 + np.exp(-new_input))


def hyperbolic_tangent(new_input: np.float32) -> np.float32:
    # normalizes the input returning a float between -1 and 1
    return np.tanh([new_input])[0]


class Perceptron:
    def __init__(self, activation_function: callable(np.float32) = None):
        self.weights = np.random.randn(2)
        self.bias = random.Random().random()
        self.activation = activation_function

    def guess(self, inputs: np.ndarray) -> np.float32:
        dot_product = np.dot(inputs, self.weights) + self.bias
        return self.activation(dot_product)
