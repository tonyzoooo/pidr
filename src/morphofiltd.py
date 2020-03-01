from numpy import array, dot, linspace, ndarray, pi, zeros
from numpy.linalg import norm


def morphofiltd(re: ndarray, order: int, r0: ndarray, r1: ndarray,
                rN: ndarray, rD: ndarray = None, Cs=1) -> ndarray:
    """
    Computes the morphofiltd

    Parameters
    ----------
    re : ndarray
        electrode positions (M x 3)
    order : int
        filter length (N+1 = nb of compartments on the axon + soma)
    r0 : ndarray
        soma position (1 x 3) (center)
    r1 : ndarray
        axon hillock position (1 x 3) (begining)
    rN : ndarray
        last axon compartment position (1 x 3) (begining)
    rD : ndarray
        tip of the equivalent dendrite (default: None)
    Cs : number
        amplitude of the somatic dipole (default: 1)

    Returns
    -------
    result : ndarray

    """

    if rD is None:
        rD = r1
    cond = 0.33
    M = re.shape[0]
    rk = array([
        linspace(r1[0], rN[0], order-1),
        linspace(r1[1], rN[1], order-1),
        linspace(r1[2], rN[2], order-1)
    ]).transpose()
    w = zeros([M, order])
    for iel in range(M):
        for ik in range(1, order-1):
            w[iel, ik] = (
                dot(-(re[iel]-rk[ik-1]), (rk[ik]-rk[ik-1]))
                / (4*pi*cond*norm(re[iel]-rk[ik-1])**3)
            )
        w[iel, order-1] = (
            dot(-(re[iel]-rk[order-2]), (rk[order-2] - rk[order-3]))
            / (4*pi*cond*norm(re[iel]-rk[order-2])**3)
        )
        w[iel, 0] = (
            -Cs * dot((re[iel]-r0), (rD-r0))
            / (4*pi*cond*norm(re[iel]-r0)**3)
        )

    return w