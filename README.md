# Fast simulation of extracellular action potential signatures based on a morphological filtering approximation

Translated from Matlab to Python (see original code [here](https://github.com/raduranta/Neural-AP-morphofilt)).

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
export PYTHONPATH=.
# Run gui
python src/gui/app.py
# Run simulation script only
python src/core/demo.py
```

After executing this command, your can load a `.hoc` file for the morphology of the cell. You can find examples in the `resources` directory.

