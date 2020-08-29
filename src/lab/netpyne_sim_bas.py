from netpyne import specs, sim

# DOCUMENTATION ----------------------------------------------------------------
''' Script generated with NetPyNE-UI. Please visit:
    - https://www.netpyne.org
    - https://github.com/MetaCell/NetPyNE-UI
'''

# SCRIPT =======================================================================
netParams = specs.NetParams()
simConfig = specs.SimConfig()

# SINGLE VALUE ATTRIBUTES ------------------------------------------------------

# NETWORK ATTRIBUTES -----------------------------------------------------------
netParams.popParams['pop'] = {
    "cellModel": "",
    "cellType": "bas",
    "numCells": 1,
    "pop": "pop"
}
netParams.cellParams['bas'] = {
    "conds": {},
    "secs": {
        "soma": {
            "geom": {
                "diam": 25,
                "L": 25,
                "Ra": 150,
                "cm": 1
            },
            "mechs": {
                "hh": {
                    "gnabar": 0.12,
                    "gkbar": 0.036,
                    "gl": 0.0003,
                    "el": -54.3
                }
            }
        },
        "dend": {
            "geom": {
                "diam": 2,
                "L": 25,
                "Ra": 150,
                "cm": 1
            },
            "mechs": {
                "pas": {
                    "g": 0.001,
                    "e": -70
                }
            },
            "topol": {
                "parentSec": "soma",
                "parentX": 0,
                "childX": 1
            }
        },
        "axon": {
            "geom": {
                "diam": 2,
                "L": 1000,
                "Ra": 150,
                "cm": 1
            },
            "topol": {
                "parentSec": "soma",
                "parentX": 1,
                "childX": 0
            },
            "mechs": {
                "hh": {
                    "gnabar": 0.12,
                    "gkbar": 0.036,
                    "gl": 0.003,
                    "el": -54.3
                }
            }
        }
    }
}
netParams.stimSourceParams['stim_source0'] = {
    "type": "IClamp",
    "del": 1,
    "dur": 10,
    "amp": 0.2
}
netParams.stimTargetParams['stim_target0'] = {
    "source": "stim_source0",
    "conds": {
        "cellList": [
            0
        ],
        "pop": [
            "pop"
        ],
        "cellType": [
            "bas"
        ]
    },
    "sec": "soma",
    "loc": 0.5
}

# NETWORK CONFIGURATION --------------------------------------------------------
simConfig.duration = 200.0
simConfig.dt = 0.1
simConfig.recordTraces = {
    "V_soma": {
        "sec": "soma",
        "loc": 0.5,
        "var": "v"
    }
}
simConfig.recordLFP = [
    [
        50,
        -250,
        0
    ],
    [
        50,
        -125,
        0
    ],
    [
        50,
        0,
        0
    ],
    [
        50,
        125,
        0
    ],
    [
        50,
        250,
        0
    ],
    [
        50,
        375,
        0
    ],
    [
        50,
        500,
        0
    ],
    [
        50,
        625,
        0
    ],
    [
        50,
        750,
        0
    ],
    [
        50,
        875,
        0
    ],
    [
        50,
        1000,
        0
    ],
    [
        50,
        1125,
        0
    ],
    [
        50,
        1250,
        0
    ],
    [
        100,
        -250,
        0
    ],
    [
        100,
        -125,
        0
    ],
    [
        100,
        0,
        0
    ],
    [
        100,
        125,
        0
    ],
    [
        100,
        250,
        0
    ],
    [
        100,
        375,
        0
    ]
]
simConfig.filename = "output"
simConfig.analysis = {
    "iplotTraces": {
        "include": [
            "all"
        ],
        "showFig": False,
        "theme": "gui"
    },
    "iplotLFP": {
        "include": [
            "all"
        ],
        "plots": [
            "spectrogram"
        ],
        "showFig": False,
        "theme": "gui",
        "electrodes": [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18
        ]
    }
}

simConfig.analysis['plotLFP'] = {'includeAxon': False, 'plots': ['timeSeries',  'locations'], 'figSize': (5,9), 'saveFig': True} 

# CREATE SIMULATE ANALYZE  NETWORK ---------------------------------------------
sim.createSimulateAnalyze(netParams=netParams, simConfig=simConfig)


# check model output
#sim.checkOutput('output')

# END SCRIPT ===================================================================
