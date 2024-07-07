# Project Structure

```angular2html
neural_network_project/
├
├── src/                    # Source code for the project
│   ├── model/              # Neural network model implementation
│   │   └── Perceptron.py
│   │   └── neural_net.py
│   ├── neural_net_test_games/  # Game to test the Neural-net
│   │   └── ...
│   ├── perceptron_game_test/  # Game to test the Perceptron
│   │   └── ...
├── requirements.txt        # Project dependencies

```

# Run environment

## Apply Conda Environment

Use Anaconda! To create an env in coda, open conda shell and:

- create and activate a conda env called neural-net
`conda create --name neural-net python=3.9`
`conda activate neural-net`

- to install packages
`conda install --file=requirements.txt`
AND/OR `pip install -r requirements.txt`


