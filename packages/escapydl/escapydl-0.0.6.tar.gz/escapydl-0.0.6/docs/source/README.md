# eSCAPyDL: SCA PyTorch Deep Learning framework

<img> ![eSCAPyDL logo](../../escapydl/resources/org/gnome/escapydl/icons/scalable/apps/escapydl-icon.svg) </img>

[![python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/downloads/release/python-360/)
[![PyPI version](https://badge.fury.io/py/escapydl.svg)](https://badge.fury.io/py/escapydl)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This framework is a framework for deep learning in the context of side-channel analysis. It is based on PyTorch and provides a set of tools to train and evaluate deep learning models for side-channel analysis.

The framework is made with customization in mind. You can easily add your own dataset, model, loss function, metrics, etc. and use them with the framework.

## Installation
```
pip install escapydl
```

## Build from source
```
git clone
(python -m venv escapydl)
python -m build
pip install dist/escapydl-*.tar.gz
```

## Structure
```
escapydl/               # Main package
├── datasets/           # Datasets, each dataset is defined in a separate file
├── helpers/            # Helper functions, useful to define cipher specific functions
├── ressources/         # Ressources for the GUI
├── Callback.py         # Callbacks for the training (e.g., guessing entropy, model checkpoint, etc.)
├── Dataset.py          # Dataset class, used to load the data
├── Models.py           # Models, all models available are defined in this file
├── Optuna_models.py    # Models for Optuna optimization
├── Utils.py            # Utility functions
├── train.py            # Script to train a model, is independent of model and dataset
├── optimize.py         # Script to optimize a model with Optuna, used to find the best hyperparameters for a given model and dataset
├── main.py             # Main script, forks to train.py, optimize.py or gui.py
├── gui.py              # Script to run the GUI
└── README.md           # This file
```

## Dataset example
```python
import helpers.aes_helper as aes

# Dataset specific parameters
parameters = {
    "training_size": 1000, # Number of traces used for training
    "val_size": 100,       # Number of traces used for validation
    ...
}

# Hyperparameters of the best known model (if it exists)
model = {
    "n_layers": 2, # Number of layers
    ...            # Other hyperparameters
}

# Define the three functions used to compute the intermediate values associated to the traces
# The first function returns the trace parameters (here, plaintext, key and subkey) for a given trace index
def get_attack_parameters(traceset, subkey, index):
    return {"plaintext": traceset.plaintext[index], 
            "key": traceset.key[index], 
            "subkey": subkey
            }

# The second function returns the real key stored in the traceset for a given trace index
def get_known_key(traceset, subkey, index):
    return traceset['key'][index][subkey]

# The third function returns the intermediate value for a given key guess and trace parameters
def intermediate_value(keyguess, trace_parameters):
    return aes.sbox[keyguess ^ trace_parameters['plaintext'][trace_parameters['subkey']]]
```

## Model example
```python
class MLP(nn.Module):
    default_Hparams = {"activation_function":'tanh',
                        "lr": 1e-3,
                        "n_layers":2,
                        "n_units_l0": 20, 
                        "n_units_l1": 10} # Default hyperparameters
    def __init__(self, trace_length,num_classes, Hparams={}):
        super(MLP, self).__init__()
        self.name = "MLP"
        self.Hparams = {**MLP.default_Hparams, **Hparams} # Merge default and given Hparams
        self.n_layers = int(self.Hparams['n_layers']) # Define the number of layers
        self.act = {"relu":nn.ReLU(), "tanh":nn.Tanh(), "selu":nn.SELU()}[self.Hparams['activation_function'].lower()] if 'activation_function' in self.Hparams.keys() else nn.ReLU() # Define the activation function
        
        # Create the PyTorch layers of the model
        self.hidden = nn.ModuleList()
        self.hidden.append(nn.Linear(trace_length, int(self.Hparams['n_units_l0'])))
        for i in range(self.n_layers-1):
            self.hidden.append(nn.Linear(int(self.Hparams['n_units_l{}'.format(i)]), int(self.Hparams['n_units_l{}'.format(i+1)])))
        self.fc1 = nn.Linear(int(self.Hparams['n_units_l{}'.format(self.n_layers-1)]), num_classes)
        self.dropout = nn.Dropout(0.1)
        self.bnorm = nn.BatchNorm1d(trace_length)
        self.flatten = nn.Flatten()

    def forward(self, x):
        # Define the forward pass
        x = self.flatten(x)
        x = self.bnorm(x)
        for i in range(self.n_layers):
            x = self.act(self.hidden[i](x))
            x = self.dropout(x)
        x = self.fc1(x)
        return x

    def fit(self,*args, **kwargs):
        # Update the default hyperparameters and the ones passed to the model.fit function and redirect to the global fit function
        if "Hparams" in kwargs.keys():
            kwargs["Hparams"] = {**kwargs["Hparams"], **self.Hparams}
        else:
            kwargs["Hparams"] = self.Hparams
        return fit(self, *args, **kwargs)
```

## Documentation
TODO

## Run
```
escapydl -d <dataset> -m <model> -t
```  
`<dataset>`: dpav42, ascad_fixed, ascad_random or aesrd  
`<model>`: cnn or mlp

or

```
escapydl -g
```  
To run the GUI

