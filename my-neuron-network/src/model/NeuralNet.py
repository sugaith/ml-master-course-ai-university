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
        output_error_gradients_over_learning_rate = output_error_gradients * self.learning_rate

        # --- update hidden to output weights and the output layer biases

        # # Calculate hidden2output Deltas
        weights_hidden2output_delta = np.matmul(output_error_gradients_over_learning_rate, inputs2hidden.transpose())

        # # Update `weights_hidden2output` with the calculated Deltas (using addition)
        self.weights_hidden2output += weights_hidden2output_delta
        # # Update the bias with the error gradient
        self.biases_output += output_error_gradients_over_learning_rate
        # todo: is the above correct??????

        # --- update inputs to hidden weights and the input biases

        # # Calculate the Hidden-layer Error
        hidden_errors = np.matmul(self.weights_hidden2output.T, output_errors)
        # # Calculate the gradient for Hidden Layer
        hidden_gradients = np.vectorize(sigmoid_gradient)(inputs2hidden)
        hidden_error_gradients = np.matmul(hidden_gradients, hidden_errors)
        hidden_gradients_over_learning_rate = np.matmul(hidden_error_gradients, self.learning_rate)

        # # Calculate input2hidden Deltas
        weights_inputs2hidden_delta = np.matmul(hidden_gradients_over_learning_rate, inputs.T)

        # # Update `weights_inputs2hidden` with the calculated Deltas (addition)
        self.weights_inputs2hidden += weights_inputs2hidden_delta
        self.biases_hidden += hidden_gradients_over_learning_rate
        # todo: is the above correct???


if __name__ == '__main__':
    nn = NeuralNet(2, 2, 1, activation=sigmoid)

    # XOR TEST
    xor_training_data = [
        {
            'inputs': np.array([0, 0]),
            'targets': np.array([0])
        },
        {
            'inputs': np.array([1, 1]),
            'targets': np.array([0])
        },
        {
            'inputs': np.array([1, 0]),
            'targets': np.array([1])
        },
        {
            'inputs': np.array([0, 1]),
            'targets': np.array([1])
        },
    ]

    for _ in range(9000):
        for data in xor_training_data:
            nn.back_propagation(data.get('inputs'), data.get('targets'))

    print(nn.feed_forward(np.array([1, 0])))
