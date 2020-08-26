#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Loïc Bertrand, Steven Le Cam, Radu Ranta, Tony Zhou
"""

from numpy import array, dot, linspace, ndarray, pi, zeros
from numpy.linalg import norm


def morphofiltd(re: ndarray, order: int, r0: ndarray, r1: ndarray,
                rN: ndarray, rD: ndarray = None, Cs=1) -> ndarray:
    """
    Performs morphological filtering approximation

    :param re:      electrode positions (M x 3)
    :param order:   filter length (N+1 = nb of compartments on the axon + soma)
    :param r0:      soma position (1 x 3) (center)
    :param r1:      axon hillock position (1 x 3) (beginning)
    :param rN:      last axon compartment position (1 x 3) (beginning)
    :param rD:      tip of the equivalent dendrite (default: None)
    :param Cs:      amplitude of the somatic dipole (default: 1)
    :return:        filtered result
    """

    if rD is None:
        rD = r1
    cond = 0.33
    M = re.shape[0]
    rk = array([
        linspace(r1[0], rN[0], order - 1),
        linspace(r1[1], rN[1], order - 1),
        linspace(r1[2], rN[2], order - 1)
    ]).T
    w = zeros([M, order])
    for iel in range(M):
        for ik in range(1, order - 1):
            w[iel, ik] = (
                    dot(-(re[iel] - rk[ik - 1]), (rk[ik] - rk[ik - 1]))
                    / (4 * pi * cond * norm(re[iel] - rk[ik - 1]) ** 3)
            )
        w[iel, order - 1] = (
                dot(-(re[iel] - rk[order - 2]), (rk[order - 2] - rk[order - 3]))
                / (4 * pi * cond * norm(re[iel] - rk[order - 2]) ** 3)
        )
        w[iel, 0] = (
                -Cs * dot((re[iel] - r0), (rD - r0))
                / (4 * pi * cond * norm(re[iel] - r0) ** 3)
        )

    return w
