import numpy as np
from src.model.activation_functions import sigmoid

class NeuralNet:
    def __init__(self, input_count: int, hidden_count: int, output_count: int, activation: callable(np.float32)):
        self.input_count = input_count
        self.hidden_count = hidden_count
        self.output_count = output_count

        self.weights_inputs2hidden: np.ndarray = np.random.randn(hidden_count, input_count)
        self.weights_hidden2output: np.ndarray = np.random.randn(hidden_count, output_count)

        print('self.weights_inputs2hidden\n', self.weights_inputs2hidden)
        print('self.weights_hidden2output\n', self.weights_hidden2output)

        self.biases_hidden: np.ndarray = np.random.randn(hidden_count)
        self.biases_output: np.ndarray = np.random.randn(output_count)

        print('self.biases_hidden\n', self.biases_hidden)
        print('self.biases_output\n', self.biases_output)

        self.activation = activation

    def feed_forward(self, inputs: np.ndarray) -> np.ndarray:
        inputs2hidden = np.matmul(inputs, self.weights_inputs2hidden)
        inputs2hidden = np.add(inputs2hidden, self.biases_hidden)
        print('inputs2hidden')
        print(inputs2hidden)
        inputs2hidden = np.vectorize(self.activation)(inputs2hidden)
        print('inputs2hidden vectorize')
        print(inputs2hidden)

        hidden2output = np.matmul(inputs2hidden, self.weights_hidden2output)
        hidden2output = np.add(hidden2output, self.biases_output)
        hidden2output = np.vectorize(self.activation)(hidden2output)

        return hidden2output












if __name__ == '__main__':
    nn = NeuralNet(2, 2, 1, activation=sigmoid)
    output = nn.feed_forward(np.array([1, 0]))
    print('output')
    print(output)