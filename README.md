# Fast simulation of extracellular action potential signatures based on a morphological filtering approximation

Translated from Matlab to Python (see original code [here](https://github.com/raduranta/Neural-AP-morphofilt)).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Run main demo
PYTHONPATH=.:src/code:src/gui python src/core/demo.py
# Run gui only
PYTHONPATH=.:src/code:src/gui python src/gui/app.py
```

After executing this command, your can load a `.hoc` file for the morphology of the cell. You can find examples in the `resources` directory.

