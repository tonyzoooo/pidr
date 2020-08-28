"""
CONFIGURATION FILE

Contains the default values used at application startup. If any of
these values or dictionary keys are missing, an error will be thrown
when launching the application.
"""

"""
Electrode grid specified as two ranges (start, stop, step),
where (-100, 150, 50) means [-100, -50, 0, 50, 100, 150].
"""
electrode_grid = {
    'xs': (-250, 1250, 125),
    'ys': (250, 50, -50),
}

"""
Stimulation parameters: amplitude (nA), duration (ms) and delay (ms).
"""
stimulation = {
    'amp': 0.2,
    'dur': 10.0,
    'delay': 1.0,
}

"""
Initially selected dimension for cell visualisations.
Possible values for 'dim' are : '2D', '3D'
"""
plot = {
    'dim': '3D'
}
