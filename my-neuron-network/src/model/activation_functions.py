import numpy as np


def sigmoid(new_input: np.float32) -> np.float32:
    # normalizes the input returning a float between 0 and 1
    return 1 / (1 + np.exp(-new_input))


def hyperbolic_tangent(new_input: np.float32) -> np.float32:
    # normalizes the input returning a float between -1 and 1
    return np.tanh([new_input])[0]
