"""
CONFIGURATION FILE

Contains default values used at application startup.
"""

"""
Electrode grid specified as two ranges (start, stop, step),
where (-100, 250, 50) means [-100, -50, 0, 50, 100, 200, 250].

Example
-------
electrode_grid = {
    'xs': (-250, 1250, 125),
    'ys': (250, 50, -50),
}
"""
electrode_grid = {
    'xs': (-250, 1250, 125),
    'ys': (250, 50, -50),
}
