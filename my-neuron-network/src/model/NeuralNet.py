import numpy as np
from src.model.activation_functions import sigmoid, sigmoid_gradient
from src.model.initialization_functons import INIT_TYPE, xavier_normal_distribution


class NeuralNet:
    def __init__(self,
                 input_count: int, hidden_count: int, output_count: int,
                 activation: callable(np.float32),
                 initialization: callable(INIT_TYPE) = None,
                 learning_rate: np.float32 = 0.1):
        self.input_count = input_count
        self.hidden_count = hidden_count
        self.output_count = output_count
        self.weights_inputs2hidden: np.ndarray = np.random.randn(hidden_count, input_count)
        self.weights_hidden2output: np.ndarray = np.random.randn(hidden_count, output_count)

        if initialization is not None:
            initialization(
                input_count, hidden_count, output_count,
                self.weights_inputs2hidden,
                self.weights_hidden2output,
            )

        self.hidden_biases: np.ndarray = np.zeros(hidden_count)
        self.output_biases: np.ndarray = np.zeros(output_count)

        self.activation = activation
        self.learning_rate = learning_rate

    def feed_forward(self, inputs: np.ndarray) -> np.ndarray:
        inputs2hidden: np.ndarray = np.matmul(inputs, self.weights_inputs2hidden.T)
        inputs2hidden += self.hidden_biases
        inputs2hidden = self.activation(inputs2hidden)

        hidden2output: np.ndarray = np.matmul(inputs2hidden, self.weights_hidden2output)
        hidden2output += self.output_biases
        hidden2output = self.activation(hidden2output)

        return hidden2output

    def back_propagation(self, inputs: np.ndarray, targets: np.ndarray):
        # --- Apply feed_forward
        inputs2hidden: np.ndarray = np.matmul(inputs, self.weights_inputs2hidden.T)
        inputs2hidden = np.add(inputs2hidden, self.hidden_biases)
        inputs2hidden = self.activation(inputs2hidden)

        hidden2output: np.ndarray = np.matmul(inputs2hidden, self.weights_hidden2output)
        hidden2output = np.add(hidden2output, self.output_biases)
        outputs = self.activation(hidden2output)

        # # Calculate errors (targets - outputs) and extract error gradients
        output_errors = np.subtract(targets, outputs)
        output_gradients = sigmoid_gradient(outputs)
        output_error_gradients = output_gradients * output_errors
        output_error_gradients_over_learning_rate = output_error_gradients * self.learning_rate

        # --- Update hidden to output weights and the output layer biases
        # Calculate hidden-to-output Deltas
        weights_hidden2output_delta = np.outer(output_error_gradients_over_learning_rate, inputs2hidden)
        # Update `weights_hidden2output` with the calculated Deltas
        self.weights_hidden2output += weights_hidden2output_delta.T
        # Update the bias with the error gradient
        self.output_biases += output_error_gradients_over_learning_rate

        # --- Update inputs-to-hidden weights and the input biases
        # Calculate errors Hidden-layer error and extract the gradients
        hidden_errors = np.matmul(self.weights_hidden2output, output_errors)
        hidden_gradients = sigmoid_gradient(inputs2hidden)
        hidden_error_gradients = hidden_gradients * hidden_errors
        hidden_gradients_over_learning_rate = hidden_error_gradients * self.learning_rate

        # Calculate input2hidden Deltas
        weights_inputs2hidden_delta = np.outer(hidden_gradients_over_learning_rate, inputs)
        # Update `weights_inputs2hidden` with the calculated Deltas
        self.weights_inputs2hidden += weights_inputs2hidden_delta
        # Update the bias with the error gradient
        self.hidden_biases += hidden_gradients_over_learning_rate


if __name__ == '__main__':
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

    nn = NeuralNet(
        2, 3, 1,
        initialization=xavier_normal_distribution,
        activation=sigmoid,
        learning_rate=np.float32(.3)
    )

    print(' UN-trained output ....  ')
    print(nn.feed_forward(np.array([0, 0])))
    print(nn.feed_forward(np.array([1, 1])))
    print(nn.feed_forward(np.array([1, 0])))
    print(nn.feed_forward(np.array([0, 1])))

    for _ in range(60000):
        for data in xor_training_data:
            nn.back_propagation(data.get('inputs'), data.get('targets'))

    for _ in range(9):
        print(str(_) + '.......')

        print(' trained output ....  ')
        print(nn.feed_forward(np.array([0, 0])))
        print(nn.feed_forward(np.array([1, 1])))
        print(nn.feed_forward(np.array([1, 0])))
        print(nn.feed_forward(np.array([0, 1])))

