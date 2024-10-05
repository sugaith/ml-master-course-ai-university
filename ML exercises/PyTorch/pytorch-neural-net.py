import torch
import torch.nn as nn
import torch.optim as optim

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Using device: {device}")


def xavier_normal_distribution(weight):
    nn.init.xavier_normal_(weight)


class NeuralNet(nn.Module):
    def __init__(self, input_count, hidden_count, output_count,
                 activation=torch.sigmoid,
                 initialization=None,
                 learning_rate=0.1):
        super(NeuralNet, self).__init__()
        self.input_count = input_count
        self.hidden_count = hidden_count
        self.output_count = output_count

        # Define layers
        self.fc1 = nn.Linear(input_count, hidden_count).to(device)
        self.fc2 = nn.Linear(hidden_count, output_count).to(device)

        # Apply initialization if provided
        if initialization is not None:
            initialization(self.fc1.weight)
            initialization(self.fc2.weight)
            nn.init.zeros_(self.fc1.bias)
            nn.init.zeros_(self.fc2.bias)

        # Activation function
        self.activation = activation
        # Optimizer
        self.learning_rate = learning_rate
        self.optimizer = optim.SGD(self.parameters(), lr=learning_rate)

        # Loss function
        self.loss_fn = nn.MSELoss()

    def forward(self, x):
        x = self.activation(self.fc1(x))
        x = self.activation(self.fc2(x))
        return x

    def train_step(self, inputs, targets):
        # Zero gradients
        self.optimizer.zero_grad()

        # Forward pass
        outputs = self.forward(inputs)

        # Compute loss
        loss = self.loss_fn(outputs, targets)

        # Backward pass
        loss.backward()

        # Update weights
        self.optimizer.step()

        return loss.item()


if __name__ == '__main__':
    # XOR training data
    xor_training_data = [
        {
            'inputs': torch.tensor([[0., 0.]]),  # Changed to 2D tensor
            'targets': torch.tensor([[0.]])
        },
        {
            'inputs': torch.tensor([[1., 1.]]),
            'targets': torch.tensor([[0.]])
        },
        {
            'inputs': torch.tensor([[1., 0.]]),
            'targets': torch.tensor([[1.]])
        },
        {
            'inputs': torch.tensor([[0., 1.]]),
            'targets': torch.tensor([[1.]])
        },
    ]

    # Create neural network
    nn_model = NeuralNet(
        input_count=2,
        hidden_count=3,
        output_count=1,
        initialization=xavier_normal_distribution,
        # activation=torch.sigmoid,
        learning_rate=0.3
    ).to(device)

    # Print untrained outputs
    print('Untrained output:')
    for data in xor_training_data:
        output = nn_model.forward(data['inputs'].to(device))
        print(f"Input: {data['inputs'].numpy()}, Output: {output.item():}")

    # Train the network
    for epoch in range(90000):
        for data in xor_training_data:
            inputs = data['inputs'].to(device)
            targets = data['targets'].to(device)
            nn_model.train_step(inputs, targets)

    # Print trained outputs
    print('\nTrained output:')
    for i in range(3):
        print(f'\nTEST N {i + 1} \n')
        for data in xor_training_data:
            output = nn_model.forward(data['inputs'].to(device))
            print(f"Input: {data['inputs'].numpy()}, Output: {output.item():}")
