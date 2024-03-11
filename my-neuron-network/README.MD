# Project Structure

```angular2html
neural_network_project/
│
├── notebooks/              # Jupyter notebooks for experiments
|   ├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_network.py
│
├── src/                    # Source code for the project
│   ├── __init__.py         # Makes src a Python module
│   ├── data/               # Scripts to download or generate data
│   │   └── __init__.py     
│   ├── model/              # Neural network model implementation
│   │   ├── __init__.py
│   │   └── perceptron.py
│   │   └── neural-net.py
│   ├── utils/              # Utility functions, e.g., for data preprocessing
│   │   ├── __init__.py
│   │   └── preprocess.py
│   └── main.py             # Entry point of the project
│
├── requirements.txt        # Project dependencies
│
└── README.md               # Project overview and setup instructions

```


# Apply Conda Environment

Use Anaconda! To create an env in coda, open conda shell and:

- create and activate a conda env called neural-net
`conda create --name neural-net python=3.9`
`conda activate neural-net`
- to install packages
`conda install --file=requirements.txt`
`pip install -r requirements.txt`


