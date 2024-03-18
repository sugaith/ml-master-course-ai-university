import random
import numpy as np


class Perceptron:
    def __init__(self, activation_function: callable(np.float32) = None):
        self.weights = np.random.randn(2)
        self.bias = random.Random().random()
        self.activation = activation_function

    def guess(self, inputs: np.ndarray) -> np.float32:
        dot_product = np.dot(inputs, self.weights)  # + self.bias
        return self.activation(dot_product)

    def train(self, inputs: np.ndarray, targets: np.float32) -> None:
        guess = self.guess(inputs)
        loss = targets - guess

        for i in range(self.weights):
            self.weights[i] += inputs[i] * loss
