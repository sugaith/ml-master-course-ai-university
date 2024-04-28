import numpy as np
from src.model.activation_functions import sigmoid, sigmoid_gradient


class NeuralNet:
    def __init__(self,
                 input_count: int, hidden_count: int, output_count: int,
                 activation: callable(np.float32),
                 learning_rate: np.float32 = 0.1):
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
        self.learning_rate = learning_rate

    def feed_forward(self, inputs: np.ndarray) -> np.ndarray:
        inputs2hidden: np.ndarray = np.matmul(inputs, self.weights_inputs2hidden)
        inputs2hidden = np.add(inputs2hidden, self.biases_hidden)
        inputs2hidden = np.vectorize(self.activation)(inputs2hidden)

        hidden2output: np.ndarray = np.matmul(inputs2hidden, self.weights_hidden2output)
        hidden2output = np.add(hidden2output, self.biases_output)
        hidden2output = np.vectorize(self.activation)(hidden2output)

        return hidden2output

    def back_propagation(self, inputs: np.ndarray, targets: np.ndarray):
        # # Apply feed_forward
        inputs2hidden: np.ndarray = np.matmul(inputs, self.weights_inputs2hidden)
        inputs2hidden = np.add(inputs2hidden, self.biases_hidden)
        inputs2hidden = np.vectorize(self.activation)(inputs2hidden)

        hidden2output: np.ndarray = np.matmul(inputs2hidden, self.weights_hidden2output)
        hidden2output = np.add(hidden2output, self.biases_output)
        outputs = np.vectorize(self.activation)(hidden2output)
        # outputs = self.feed_forward(inputs)
        print('outputs\n', outputs)

        # # Calculate errors (targets - outputs)
        output_errors = np.subtract(targets, outputs)
        print('ERROR: ')
        print(output_errors)

        # # Calculate error gradient:
        # apply sigmoid derivative (gradient) to outputs
        # multiply output gradient by the error
        # multiply again by the learning rate
        output_gradients = np.vectorize(sigmoid_gradient)(outputs)
        output_error_gradients = np.matmul(output_gradients, output_errors)
        output_error_gradients_over_learning_rate = np.matmul(output_error_gradients, self.learning_rate)

        # # Calculate hidden2output Deltas
        transposed_hidden = np.transpose(inputs2hidden)
        weights_hidden2output_delta = np.matmul(output_error_gradients_over_learning_rate, transposed_hidden)

        # # Update `weights_hidden2output` with the calculated Deltas (using addition)
        # todo: is this correct??????
        self.weights_hidden2output += weights_hidden2output_delta

        # # Calculate the Hidden-layer Error
        weights_hidden2output_transposed = np.transpose(self.weights_hidden2output)
        hidden_errors = np.matmul(weights_hidden2output_transposed, output_errors)

        # # Calculate the gradient for Hidden Layer
        hidden_gradients = np.vectorize(sigmoid_gradient)(inputs2hidden)
        hidden_error_gradients = np.matmul(hidden_gradients, hidden_errors)
        hidden_gradients_over_learning_rate = np.matmul(hidden_error_gradients, self.learning_rate)

        # # Calculate input2hidden Deltas
        transposed_inputs = np.transpose(inputs)
        weights_inputs2hidden_delta = np.matmul(hidden_gradients_over_learning_rate, transposed_inputs)

        # # Update `weights_inputs2hidden` with the calculated Deltas (addition)
        # todo: is this correct???
        self.weights_inputs2hidden += weights_inputs2hidden_delta








if __name__ == '__main__':
    nn = NeuralNet(2, 2, 2, activation=sigmoid)
    output = nn.back_propagation(np.array([1, 0]), np.array([0.5, 0.5]))
    # print('output')
    # print(output)