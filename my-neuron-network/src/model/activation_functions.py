import numpy as np


def sigmoid(new_input: np.float32 | np.ndarray) -> np.float32 | np.ndarray:
    # normalizes the input returning a float between 0 and 1
    return 1 / (1 + np.exp(-new_input))


def sigmoid_gradient(sigmoid_input: np.float32 | np.ndarray) -> np.float32 | np.ndarray:
    return sigmoid_input * (np.float32(1) - sigmoid_input)


def hyperbolic_tangent(new_input: np.float32 | np.ndarray) -> np.float32 | np.ndarray:
    # normalizes the input returning a float between -1 and 1
    return np.tanh([new_input])[0]


def step(new_input: np.float32) -> int:
    ht = hyperbolic_tangent(new_input)
    return 1 if ht > 0 else 0
