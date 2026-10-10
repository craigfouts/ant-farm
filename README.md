# Ant Farm - Experiments with Self-Organizing Systems

[![Asterism](https://github.com/craigfouts/ant-farm/actions/workflows/antfarm.yml/badge.svg?event=push)](https://github.com/craigfouts/ant-farm/actions/workflows/antfarm.yml) [![License](https://img.shields.io/badge/License-Apache_2.0-red.svg)](https://opensource.org/licenses/Apache-2.0) [![Python](https://img.shields.io/badge/Python-3.14.7-blue)](https://www.python.org/downloads/release/python-3147/)

**Ant farm** is a collection of experiments with self-organizing systems and emergent behavior. Current methods include a Brownian motion algorithm, a Vicsek active matter model, and a branching-annihilating random walk. It also serves as a test bed for **RunTime**, a framework for building real-time interactive environments in Jupyter notebooks.

## Installation

### MacOS

```bash
git clone https://github.com/craigfouts/ant-farm.git
cd ant-farm
python -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
git clone https://github.com/craigfouts/ant-farm.git
cd asterism
python -m venv .env
.env\Scripts\activate
pip install -r requirements.txt
```

## Usage

```python
from antfarm import NBody

NBody().record(path='output/nbody.mp4', show=True)
```

<video alt="video" src="https://github.com/user-attachments/assets/e0a48752-b198-49c9-89cf-b149bcfbb9d8" />

Additional examples are provided in ```notebooks/demos.ipynb```
