import random
import numpy as np


class Perceptron:
    def __init__(self,
                 activation_function: callable(np.float32) = None,
                 number_of_params: int = 2,
                 learning_rate: np.float32 = np.float32(.00009),
                 ):
        self.weights: np.array = np.random.rand(number_of_params)
        self.bias: np.float32 = np.float32(random.random())
        self.learning_rate: np.float32 = learning_rate
        self.activation = activation_function

    def guess(self, inputs: np.array) -> np.float32:
        dot_product = np.dot(inputs, self.weights) + self.bias
        return self.activation(dot_product)

    def train(self, inputs: np.array, targets: np.float32) -> None:
        guess = self.guess(inputs)
        loss = targets - guess

        self.bias += loss * self.learning_rate

        for i in range(self.weights.size):
            self.weights[i] += inputs[i] * loss * self.learning_rate



