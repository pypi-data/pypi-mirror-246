# module

This library allows you to create small subsections of a larger network (to be executed on a remote server)

## Installation
You can install using either pip or conda
### Install using pip
```shell
pip install moduler
```

### Install using conda
```shell
conda install moduler
```

## Usage

Example with Pytorch

```python
import os
import moduler as md
import torch.nn as nn

os.environ["BABS_API_KEY"] = ""

model = nn.Sequential(
    md.base.Llama(),  # this will be executed remotely (forward-pass only)
    nn.Linear(in_features=20, out_features=40)  # this module will run locally (forward and backward pass)
)
model.train()
```

Example with Tensorflow

```python
import os
import moduler as md
import tensorflow as tf

os.environ["BABS_API_KEY"] = ""
model = 
```