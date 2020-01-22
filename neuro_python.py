from numpy import linspace, size, zeros, pi, array, exp, arange, heaviside
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
    rk = [linspace(r1[0],rN[0],ordre-1), linspace(r1[1],rN(1),ordre-1), linspace(r1[2],rN[2],ordre-1)]
    w = zeros(M, ordre)
    for iel in range(M) :
        for ik in range(1,ordre-1) :
            w[iel,ik]=-(re[iel,:]-rk[ik-1,:])*(rk[ik,:]-rk[ik-1,:])/(4*pi*cond*norm(re[iel,:]-rk[ik-1,:])**3)
        w[iel,ordre]=-(re[iel,:]-rk[ordre-1,:])*(rk[ordre-1,:]-rk[ordre-2,:])/(4*pi*cond*norm(re[iel,:]-rk[ordre-1,:])**3)
        w[iel,1]=-Cs*(re[iel,:]-r0)*(rD-r0)/(4*pi*cond*norm(re[iel,:]-r0)**3)
    return w

def hhrun(I, t):
        # function a=am(v) 
    # #Alpha for Variable m
    # a=0.1*(v+35)/(1-exp(-(v+35)/10));
    # end
    # 
    # function b=bm(v) 
    # #Beta for variable m
    # b=4.0*exp(-0.0556*(v+60));
    # end
    # 
    # function a=an(v)
    # #Alpha for variable n
    # a=0.01*(v+50)/(1-exp(-(v+50)/10));
    # end
    # 
    # function b=bn(v) 
    # #Beta for variable n
    # b=0.125*exp(-(v+60)/80);
    # end
    # 
    # function a=ah(v) 
    # #Alpha value for variable h
    # a=0.07*exp(-0.05*(v+60));
    # end
    # 
    # function b =bh(v) 
    # #beta value for variable h
    # b=1/(1+exp(-(0.1)*(v+30)));
    # end

    ## Gerstner page EPFL
    def create_am(v):
    #Alpha for Variable m
        v=v+65
        a=(2.5-0.1*v)/(exp(2.5-0.1*v)-1)
        if v==25:
            a=1/2*((2.5-0.1*(v-1))/(exp(2.5-0.1*(v-1))-1)+(2.5-0.1*(v+1))/(exp(2.5-0.1*(v+1))-1))
        return a

    def create_bm(v):

    #Beta for variable m
        v=v+65
        b=4*exp(-v/18)
        return b

    def create_an(v):
    #Alpha for variable n
        v=v+65
        a=(0.1-0.01*v)/(exp(1-0.1*v)-1)
        if v==10:
            a=1/2*((0.1-0.01*(v-1))/(exp(1-0.1*(v-1))-1)+(0.1-0.01*(v+1))/(exp(1-0.1*(v+1))-1))
        return a

    def create_bn(v):
    #Beta for variable n
        v=v+65
        b=0.125*exp(-v/80)
        return b

    def create_ah(v):
    #Alpha value for variable h
        v=v+65
        a=0.07*exp(-v/20)
        return a

    def create_bh(v): 
    #beta value for variable h
        v=v+65
        b=1/(exp(3-0.1*v)+1)
        if v==30:
            b=1/2*(1/(exp(3-0.1*(v-1))+1)+1/(exp(3-0.1*(v+1))+1))
        return b


    #Constants set for all Methods
    # dt=0.04; # Time Step ms
    # t=0:dt:25; #Time Array ms
    # I=0.1; #External Current Applied
    dt=t[1]-t[0]

    # Cm=0.01; # Membrane Capcitance uF/cm**2
    # ENa=55.17; # mv Na reversal potential
    # EK=-72.14; # mv K reversal potential
    # El=-49.42; # mv Leakage reversal potential
    # gbarNa=1.2; # mS/cm**2 Na conductance
    # gbarK=0.36; # mS/cm**2 K conductance
    # gbarl=0.003; # mS/cm**2 Leakage conductance
    # V(1)=-60; # Initial Membrane voltage

    # # params from Gerstner EPFL page
    # Cm=1/200000; # uF/cm**2 / uF/mm2 divisé par 100, etc
    # ENa=115-65; # mv Na reversal potential
    # EK=-12-65; # mv K reversal potential
    # El=10.6-65; # mv Leakage reversal potential
    # gbarNa=120/200000; # mS/cm**2 Na conductance
    # gbarK=36/200000; # mS/cm**2 K conductance
    # gbarl=0.3/200000; # mS/cm**2 Leakage conductance
    # V(1)=-65; # Initial Membrane voltage

    # params from Gerstner EPFL page (http://icwww.epfl.ch/~gerstner/SPNM/node14.html)
    Cm=1 # uF/cm**2 / uF/mm2 divisé par 100, etc
    ENa=115-65 # mv Na reversal potential
    EK=-12-65 # mv K reversal potential
    El=10.7-65 # mv Leakage reversal potential
    gbarNa=120 # mS/cm**2 Na conductance
    gbarK=36 #36# mS/cm**2 K conductance
    gbarl=0.3 # mS/cm**2 Leakage conductance
    V[0]=-65 # Initial Membrane voltage

    m[0]=am(V[0])/(am(V[0])+bm(V[0])) # Initial m-value
    n[1]=an(V[0])/(an(V[1])+bn(V[0])) # Initial n-value
    h[1]=ah(V[0])/(ah(V[0])+bh(V[0]))# Initial h-value
    for i in range(length(t)):
        #Euler method to find the next m/n/h value
        m[i+1]=m[i]+dt*((am(V[i])*(1-m[i]))-(bm(V[i])*m[i]))
        n[i+1]=n[i]+dt*((an(V[i])*(1-n[i]))-(bn(V[i])*n[i]))
        h[i+1]=h[i]+dt*((ah(V[i])*(1-h[i]))-(bh(V[i])*h[i]))
        gNa=gbarNa*m[i]**3*h[i]
        gK=gbarK*n[i]**4
        gl=gbarl
        INa[i]=gNa*(V[i]-ENa)
        IK[i]=gK*(V[i]-EK)
        Il[i]=gl*(V[i]-El)
        #Euler method to find the next voltage value
        V[i+1]=V[i]+(dt)*((1/Cm)*(I[i]-(INa[i]+IK[i]+Il[i])))
    INa[i+1]=gNa*(V[i+1]-ENa)
    IK[i+1]=gK*(V[i+1]-EK)
    Il[i+1]=gl*(V[i+1]-El)
  
    # #Store variables for graphing later
    # FE=V;
    # FEm=m;
    # FEn=n;
    # FEh=h;
    # clear V m n h;
    return [V,m,n,h,INa,IK,Il]

#Programme principal
## HH
inmvm=3000 #index max on Vm in LFPy (3000 for synchronisation)
lVLFPy=8000 #signal length in LFPy
dt=10**(-3) #in ms
Nt=2**15
D=Nt*dt
t=arange(dt, D, dt)-dt
n=len(t)

fe=1/dt
f=arange(0, fe/2-fe/Nt, fe/Nt)

I=(heaviside(t-1, 1/2)-heaviside(t-31, 1/2))*0.044/(2*pi*12.5*25)*10**8*10**-3 #*5.093;%0.15/(pi*12.5*12.5*2+2*pi*12.5*25)*10**8;
icur=1
[Vm,m,n,h,INa,IK,Il]=hhrun(I,t) # pot membrane, proportionnel au courant des canaux ioniques (http://www.bem.fi/book/03/03.htm, 3.14)
Im=(INa+IK+Il)*(2*pi*12.5*25)/10**8*10**3
[MVm,inMVm]=max(Vm)

## BS neuron morphology

SL=25 # soma length (cylinder with the same diameter)

LA=1000# %axon length
DA=2# %axon diameter

LD=50#dendrite length 
DD=2#dendrite diameter
phi=pi/2# angle avec Oz
theta=pi# angle with Ox (phi=pi/2,theta=pi) indicates opposite to the axon

##load LFPy simulation result
"""
Vlfpy=dlmread(['../Python/Vlfpy_BS_LA',num2str(LA),'_DA',num2str(DA),'_LD',num2str(LD),'_DD',num2str(DD),'demo.txt']);
Vmlfpy=dlmread(['../Python/Vm_BS_LA',num2str(LA),'_DA',num2str(DA),'_LD',num2str(LD),'_DD',num2str(DD),'demo.txt']);
Imlfpy=dlmread(['../Python/Im_BS_LA',num2str(LA),'_DA',num2str(DA),'_LD',num2str(LD),'_DD',num2str(DD),'demo.txt']);

%% figure check
figure
subplot(2,1,1)
plot(Vm([inMVm-inmvm+1:inMVm-inmvm+lVLFPy])) 
hold on
plot(Vmlfpy)

subplot(2,1,2)
plot(Im([inMVm-inmvm+1:inMVm-inmvm+lVLFPy]))
hold on
plot(Imlfpy)


%% filter parameters
dk=10; % axonal spatial sampling (~ nb of segments)
ordre=LA/dk+1;
r0=[0 0 0]; % soma position
r1=[SL/2 0 0]; % axon start position
rN=[SL/2+LA-dk 0 0]; % axon stop position (start of the last segment)
rd=norm(r1-r0)*[sin(phi)*cos(theta) sin(phi)*sin(theta) cos(phi)]; % dendrite end position, normalized
Cs=2; % somatic equivalent dipole amplitude
taus=23; % subsampling of the membrane current dk/taus = speed v)

%% electrodes
X=[-250:125:1250]';
Y=[250:-50:50]';
Z=0;

[eplosy,elposx,elposz]=meshgrid(Y,X,Z);
elpos=[elposx(:),eplosy(:),elposz(:)]

%% simulation
w = morphofiltd(elpos,ordre,r0,r1,rN,rd,Cs);
wup=upsample(w',taus)';

Vel=zeros(size(w,1),length(Im));
for iel=1:size(w,1),
    Vel(iel,:)=conv(Im,wup(iel,:),'same');
end
% cut
intervVm=[inMVm-inmvm-fix(size(wup,2)/2)+1:inMVm-inmvm-fix(size(wup,2)/2)+lVLFPy];
Vel2=Vel(:,intervVm);
% normalize
elsync=56;
Vel2=Vel2/norm(Vel2(elsync,:))*norm(Vlfpy(:,elsync));
%% plot grid 

cc=zeros(1,size(elpos,1));
t=dt:dt:dt*size(Vel2,2);
figure
cmap=colormap;
for ifil=1:size(elpos,1),
    subplot(5,13,ifil);
    plot(t,Vel2(ifil,:)-Vel2(ifil,1),'LineWidth',2)
    hold on
    plot(t,Vlfpy(:,ifil)-Vlfpy(1,ifil),'LineWidth',2)
    cc(ifil)=corr(Vel2(ifil,:)',Vlfpy(:,ifil));
    scatter(4,-2*10**-3,100,cmap(1+fix(size(cmap,1)*cc(ifil)),:),'filled')
    ylim([-5 5]*10**-3)
    if ifil>52
        text(2,-12*10**-3,[num2str((ifil-53)*125-250),'\mu','m'])
    end
    if rem(ifil,13)==1,
       text(-8,0*10**-3,[num2str(-fix(ifil/13)*50+250),'\mu','m'])
    end 
    axis off
end
colorbar('Position',[0.93 0.3 0.007 0.6],'FontSize',14)

fprintf('\n Mean correlation = %1.2f \n Min correlation = %1.2f  \n Max correlation = %1.2f \n',mean(cc),min(cc),max(cc))
"""