# Fast simulation of extracellular action potential signatures based on a morphological filtering approximation

Based on original code from [here](https://github.com/raduranta/Neural-AP-morphofilt).

## Installation

```bash
pip install -r requirements.txt
```

You may have to install some of the required packages through your package manager (on Linux) for the app to work correctly, especially `mayavi` and `neuron`.

## Usage

```bash
export PYTHONPATH=.
# Running gui
python src/app/main.py
# Running simulation script only
python src/core/demo.py
# Running simulation script (NetPyNE)
python src/core/demo2.py
```

## GUI guide

### 'Morphology' tab

In this tab, you can create a *ball & stick* cell morphology or select a HOC file to load. You can switch between the two by clicking on the buttons **`Use HOC file`** and **`Use builder`**. The selected source will be used to display the cell and for the simulation. 

To create a morphology, enter the name for a section under 'New section' an press Enter or click on **`Create`**. A new section with the given name appears in the list. You can then customize the selected section using the fields on the right.

The **`Autofill`** button fills the builder with a basic *ball & stick* morphology (soma, axon and one dendrite).

You can save your morphology in HOC format by clicking on the **`Save to file`** button.

### 'Stimulation' tab

In this tab, you can parameterize the stimulation. Its position can be specified with two diffrent modes:
- the **`closest`** mode allows you to select the segment of the cell which is closest to a given point in 3D space ;
- the **`section`** mode allows you to directly select a segment from a given section of the cell.

### 'Recording' tab

This tab is used to set the position of the recording electrodes. They are aranged in a grid, specified by two closed ranges: one for the ***x*-axis** and one for the ***y*-axis**.

*Example:*
```
        start  stop  step
    xs [ -10 ][ 30 ][ 10 ] μm
    ys [ 150 ][ 50 ][-50 ] μm

    -10    0   10   20   30  
150   ·    ·    ·    ·    ·    ^ y
100   ·    ·    ·    ·    ·    │    x
 50   ·    ·    ·    ·    ·    └────>
```

### Right side buttons

The **`Display`** button renders the cell morphology in 2D or 3D depending on the radio button selected above. The **`Simulation`** button launches the comparison script between LFPy's simulation and Tran's simplified simulation.

These two buttons only work if a cell morphology has been specified in the 'Morphology' tab.

### Configuration file

The file [`src/app/config.py`](src/app/config.py) is used to specify a default value for certain fields of the application. The properties of this file are all mandatory because they are used to initialize fields at application startup.
