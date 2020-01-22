from numpy import linspace, size, zeros, pi
from numpy.linalg import norm

def morphofiltd(re, ordre, r0, r1, rN, rD = None, Cs = 1) :
    """inputs: 
        elpos = electrode positions (M x 3)
        ordre = filter length (N+1 = nb of compartments on the axon + soma)
        r0 = soma position (1 x 3) (center)
        r1 = axon hillock position (1 x 3) (begining)
        rN = last axon compartment position (1 x 3) (begining)
        rD = tip of the equivalent dendrite
        Cs = amplitude of the somatic dipole"""
    
    if rD is None:
        rD = r1
    cond = 0.33
    M = size(re, 0)
    rk = [linspace(r1[0],rN[0],ordre-1), linspace(r1[1],rN(1),ordre-1), linspace(r1[2],rN[2],ordre-1)].H
    w = zeros(M, ordre)
    for iel in range(M) :
        for ik in range(1,ordre-1) :
            w[iel,ik]=-(re[iel,:]-rk[ik-1,:])*(rk[ik,:]-rk[ik-1,:]).H/(4*pi*cond*norm(re[iel,:]-rk[ik-1,:])^3)
        w[iel,ordre]=-(re[iel,:]-rk[ordre-1,:])*(rk[ordre-1,:]-rk[ordre-2,:]).H/(4*pi*cond*norm(re[iel,:]-rk[ordre-1,:])^3)
        w[iel,1]=-Cs*(re[iel,:]-r0)*(rD-r0).H/(4*pi*cond*norm(re[iel,:]-r0)^3)
    return w