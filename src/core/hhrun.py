from typing import Tuple

from numpy import exp, zeros
from numpy.core.multiarray import ndarray


def hhrun(I: ndarray, t: ndarray) -> Tuple[ndarray, ...]:
    """
    Performs Hodgkin–Huxley algorithm

    Returns
        - V:    membrane voltage (mV)
        - m:    ?
        - n:    ?
        - h:    ?
        - INa:  sodium ionic currents
        - IK:   potassium ionic currents
        - Il:   leakage currents

    :param I:   stimulation intensity vector
    :param t:   time vector
    :return (V, m, n, h, INa, IK, Il)
    """

    print('I', I)
    for i in I:
        print(i)

    # def am(v):
    #     # Alpha for Variable m
    #     a = 0.1*(v+35)/(1-exp(-(v+35)/10))
    #     return a

    # def bm(v):
    #     # Beta for variable m
    #     b = 4.0*exp(-0.0556*(v+60))
    #     return b

    # def an(v):
    #     # Alpha for variable n
    #     a = 0.01*(v+50)/(1-exp(-(v+50)/10))
    #     return a

    # def bn(v):
    #     # Beta for variable n
    #     b = 0.125*exp(-(v+60)/80)
    #     return b

    # def ah(v):
    #     # Alpha value for variable h
    #     a = 0.07*exp(-0.05*(v+60))
    #     return a

    # def bh(v):
    #     # beta value for variable h
    #     b = 1/(1+exp(-(0.1)*(v+30)))
    #     return b

    # -------------------------------------------------------
    # Gerstner page EPFL
    # -------------------------------------------------------

    def am(v):
        # Alpha for Variable m
        v = v+65
        a = (2.5-0.1*v)/(exp(2.5-0.1*v)-1)
        if v == 25:
            a = 1/2*((2.5-0.1*(v-1))/(exp(2.5-0.1*(v-1))-1) +
                     (2.5-0.1*(v+1))/(exp(2.5-0.1*(v+1))-1))
        return a

    def bm(v):
        # Beta for variable m
        v = v+65
        b = 4*exp(-v/18)
        return b

    def an(v):
        # Alpha for variable n
        v = v+65
        a = (0.1-0.01*v)/(exp(1-0.1*v)-1)
        if v == 10:
            a = 1/2*((0.1-0.01*(v-1))/(exp(1-0.1*(v-1))-1) +
                     (0.1-0.01*(v+1))/(exp(1-0.1*(v+1))-1))
        return a

    def bn(v):
        # Beta for variable n
        v = v+65
        b = 0.125*exp(-v/80)
        return b

    def ah(v):
        # Alpha value for variable h
        v = v+65
        a = 0.07*exp(-v/20)
        return a

    def bh(v):
        # beta value for variable h
        v = v+65
        b = 1/(exp(3-0.1*v)+1)
        if v == 30:
            b = 1/2*(1/(exp(3-0.1*(v-1))+1)+1/(exp(3-0.1*(v+1))+1))
        return b

    # Constants set for all Methods
    # dt = 0.04                 # Time Step ms
    # t = arange(0, 25+dt, dt)  # Time Array ms
    # I = 0.1                   # External Current Applied
    dt = t[1]-t[0]

    # Array initializations
    length = len(t)
    V = zeros(length)
    m = zeros(length)
    n = zeros(length)
    h = zeros(length)
    INa = zeros(length)
    IK = zeros(length)
    Il = zeros(length)

    # Cm = 0.01       # Membrane Capcitance uF/cm**2
    # ENa = 55.17     # mv Na reversal potential
    # EK = -72.14     # mv K reversal potential
    # El = -49.42     # mv Leakage reversal potential
    # gbarNa = 1.2    # mS/cm**2 Na conductance
    # gbarK = 0.36    # mS/cm**2 K conductance
    # gbarl = 0.003   # mS/cm**2 Leakage conductance
    # V[1] = -60      # Initial Membrane voltage

    # # params from Gerstner EPFL page
    # Cm = 1/200000       # uF/cm**2 / uF/mm2 divisé par 100, etc
    # ENa = 115-65        # mv Na reversal potential
    # EK = -12-65         # mv K reversal potential
    # El = 10.6-65        # mv Leakage reversal potential
    # gbarNa = 120/200000 # mS/cm**2 Na conductance
    # gbarK = 36/200000   # mS/cm**2 K conductance
    # gbarl = 0.3/200000  # mS/cm**2 Leakage conductance
    # V[1] = -65          # Initial Membrane voltage

    # params from Gerstner EPFL page (http://icwww.epfl.ch/~gerstner/SPNM/node14.html)
    Cm = 1          # uF/cm**2 / uF/mm2 divisé par 100, etc
    ENa = 115-65    # mv Na reversal potential
    EK = -12-65     # mv K reversal potential
    El = 10.7-65    # mv Leakage reversal potential
    gbarNa = 120    # mS/cm**2 Na conductance
    gbarK = 36      # 36# mS/cm**2 K conductance
    gbarl = 0.3     # mS/cm**2 Leakage conductance
    V[0] = -65      # Initial Membrane voltage

    m[0] = am(V[0]) / (am(V[0]) + bm(V[0]))  # Initial m-value
    n[0] = an(V[0]) / (an(V[0]) + bn(V[0]))  # Initial n-value
    h[0] = ah(V[0]) / (ah(V[0]) + bh(V[0]))  # Initial h-value
    for i in range(length - 1):
        # Euler method to find the next m/n/h value
        m[i + 1] = m[i] + dt * ((am(V[i]) * (1 - m[i])) - (bm(V[i]) * m[i]))
        n[i + 1] = n[i] + dt * ((an(V[i]) * (1 - n[i])) - (bn(V[i]) * n[i]))
        h[i + 1] = h[i] + dt * ((ah(V[i]) * (1 - h[i])) - (bh(V[i]) * h[i]))
        gNa = gbarNa * m[i] ** 3 * h[i]
        gK = gbarK * n[i] ** 4
        gl = gbarl
        INa[i] = gNa * (V[i] - ENa)
        IK[i] = gK * (V[i] - EK)
        Il[i] = gl * (V[i] - El)
        # Euler method to find the next voltage value
        V[i + 1] = V[i] + dt * ((1 / Cm) * (I[i] - (INa[i] + IK[i] + Il[i])))
    INa[i + 1] = gNa * (V[i + 1] - ENa)
    IK[i + 1] = gK * (V[i + 1] - EK)
    Il[i + 1] = gl * (V[i + 1] - El)

    return V, m, n, h, INa, IK, Il
