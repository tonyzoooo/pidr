import LFPy

morphology = '../../resources/BSR_LA1000_DA2_LD50_DD2_demo.hoc'
st = 1 / 1000
cell_parameters = {
    'morphology': morphology,
    'v_init': -65,  # Initial membrane potential. Defaults to -70 mV
    'passive': True,  # Passive mechanisms are initialized if True
    'passive_parameters': {'g_pas': 1. / 30000, 'e_pas': -65},
    'cm': 1.0,  # Membrane capacitance
    'Ra': 150,  # Axial resistance
    'dt': st,  # simulation timestep
    'tstart': 0.,  # Initialization time for simulation <= 0 ms
    'tstop': 20.,  # Stop time for simulation > 0 ms
    'nsegs_method': 'lambda_f',  # spatial discretization method
    'lambda_f': 100.,  # frequency where length constants are computed
}
cell = LFPy.Cell(**cell_parameters)

print('---cell.get_idx')
print('allsec', cell.get_idx('allsec'))
print('soma', cell.get_idx('soma'))
print('axon', cell.get_idx('axon'))
print('dend', cell.get_idx('dend'))

print('---cell.get_closest_idx')
print('(0, 0, 0)', cell.get_closest_idx(0, 0, 0))

amp = 0.2
dur = 10
delay = 1

stim = {
    'idx': cell.get_closest_idx(x=0, y=0, z=0),
    'record_current': True,
    'pptype': 'IClamp',  # Type of point process: VClamp / SEClamp / ICLamp.
    'amp': amp,
    'dur': dur,
    'delay': delay,
}
stimulus = LFPy.StimIntElectrode(cell, **stim)
