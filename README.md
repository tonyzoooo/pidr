# Fast simulation of extracellular action potential signatures based on a morphological filtering approximation

Based on original code [here](https://github.com/raduranta/Neural-AP-morphofilt).

## Installation

```bash
pip install -r requirements.txt
```

Note: you may have to install some of the required packages through your package manager (on Linux) for the app to work.

## Usage

```bash
export PYTHONPATH=.
# Run gui
python src/app/main.py
# Run simulation script only
python src/core/demo.py
```

## GUI guide

### Morphology tab

In this tab, you can create a 'ball & stick' cell morphology or load an HOC file. You can switch between the two by clicking on the buttons 'Use HOC file' and 'Use builder'. The selected source will be used to display the cell and for the simulation. The 'Example' button auto-fills the builder with a basic 'ball & stick' morphology (soma, axon and one dendrite).

### Stimulation tab

In this tab, you can parameterize the stimulation. The 'closest' mode allows you to select the segment of the cell which is closest to a given point in 3D space. The 'section' mode allows you to directly select a segment from a given section of the cell.

### Right side buttons

The 'Display' button renders the cell morphology in 2D or 3D depending on the radio button selected above. The 'Simulation' button launches the comparison script between LFPy's simulation and Tran's simplified simulation.