import numpy as np


def xavier_normal_distribution(
        input_count: int,
        hidden_count: int,
        output_count: int,
        weights_inputs2hidden_ref: np.ndarray,
        weights_hidden2output_ref: np.ndarray,
):
    standard_deviation_hidden = np.sqrt(1. / hidden_count)
    standard_deviation_output = np.sqrt(1. / output_count)

    weights_inputs2hidden_ref[:] = np.random.randn(input_count, hidden_count) * standard_deviation_hidden
    weights_hidden2output_ref[:] = np.random.randn(output_count, hidden_count) * standard_deviation_output


def xavier_uniform_distribution(
        input_count: int,
        hidden_count: int,
        output_count: int,
        weights_inputs2hidden_ref: np.ndarray,
        weights_hidden2output_ref: np.ndarray,
):
    limit_hidden = np.sqrt(1. / hidden_count)
    limit_output = np.sqrt(1. / output_count)

    weights_inputs2hidden_ref[:] = np.random.uniform(-limit_hidden, limit_hidden, (hidden_count, input_count))
    weights_hidden2output_ref[:] = np.random.uniform(-limit_output, limit_output, (output_count, hidden_count))
