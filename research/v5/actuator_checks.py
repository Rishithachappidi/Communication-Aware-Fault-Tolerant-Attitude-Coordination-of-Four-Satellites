"""Independent finite-model RK4/impulse/stage calculation; no simulator import."""
from independent_checks import *
from scipy.linalg import expm

def map_parts(c,jf,tf):
 J=c['J']*jf;tau=c['tau']*tf;J0=c['J'];d=c['b'];kp=c['kp'];kd=c['kd'];ki=c['ki'];dt=c['dt']
 A=np.array([[0,1,0,0],[0,-d/J,1/J,0],[-J0*kp/tau,(d-J0*kd)/tau,-1/tau,-J0*ki/tau],[1,0,0,0]])
 B=np.array([[0,0,0],[0,0,0],[J0*kp/tau,-J0*kp/tau,(d-J0*kd)/tau],[-1,1,0]])
 # Compute RK4 stages by explicit slope recurrence, not an augmented exp polynomial.
 def step(x,u):
  k1=A@x+B@u;k2=A@(x+dt/2*k1)+B@u;k3=A@(x+dt/2*k2)+B@u;k4=A@(x+dt*k3)+B@u
  return x+dt/6*(k1+2*k2+2*k3+k4)
 Ad=np.column_stack([step(np.eye(4)[:,i],np.zeros(3)) for i in range(4)]);Bd=np.column_stack([step(np.zeros(4),np.eye(3)[:,i]) for i in range(3)])
 return A,B,Ad,Bd

def main():
 d=loadmat(OUT/'actuator_reference.mat',simplify_cells=True);c=d['c'];L=d['L'];N=int(np.ceil(c['T']/c['dt']));w=c['kappa']*np.array([c['noise'],2*c['noise']]);m=0;maperr=0.;tubeerr=0.;constraintchecks=0
 Cs=np.array([-c['J']*c['kp'],c['b']-c['J']*c['kd'],0,-c['J']*c['ki']]);models=[]
 for jf in c['Jfactors']:
  for tf in c['taufactors']:
   A,B,Ad,Bd=map_parts(c,jf,tf);maperr=max(maperr,float(np.max(np.abs(Ad-d['AD'][:,:,m]))),float(np.max(np.abs(Bd-d['BD'][:,:,m]))));m+=1
   # Explicit stage maps and finite noise convolution.
   H=[np.eye(4)];K=[np.zeros((4,3))]
   for factor in [c['dt']/2,c['dt']/2,c['dt']]:H.append(np.eye(4)+factor*A@H[-1]);K.append(factor*(A@K[-1]+B))
   impulse=Bd[:,1:].copy();state=np.zeros(4);raw=np.zeros(4);rate=np.zeros(4)
   for n in range(N):
    state+=np.abs(impulse)@w
    for s in range(4):raw[s]+=np.abs(Cs@H[s]@impulse)@w;rate[s]+=np.abs(H[s][1]@impulse)@w
    impulse=Ad@impulse
   for s in range(4):raw[s]+=np.abs(Cs@K[s][:,1:]+np.array([-c['J']*c['kp'],c['b']-c['J']*c['kd']]))@w;rate[s]+=np.abs(K[s][1,1:])@w
   models.append((Ad,Bd,H,K,state,raw,rate))
 for candidate in np.atleast_1d(L):
  t=candidate['time'];refs=candidate['q'][np.minimum(7,np.floor((t+1e-9)/candidate['dwell']).astype(int))];nom=np.zeros((4,2));An,Bn=map_parts(c,1,1)[2:];motion=[]
  for ref in refs:motion.append(nom[0].copy());nom=An@nom+Bn[:,0,None]*ref
  motion=np.array(motion);np.testing.assert_allclose(motion,candidate['motion'],atol=1e-17)
  enclosure=np.zeros(len(t));valid=True
  for Ad,Bd,H,K,state,raw,rate in models:
   mean=np.zeros((4,2))
   for i,ref in enumerate(refs):
    enclosure[i]=max(enclosure[i],np.linalg.norm(mean[0]-motion[i])+math.sqrt(2)*state[0])
    for s in range(4):
     st=H[s]@mean+K[s][:,0,None]*ref;u=Cs@st+c['J']*c['kp']*ref
     valid=valid and bool(np.all(np.abs(u)+raw[s]<c['umax']) and np.all(np.abs(st[1])+rate[s]<c['rateMax']));constraintchecks+=1
    mean=Ad@mean+Bd[:,0,None]*ref
  tubeerr=max(tubeerr,float(np.max(np.abs(enclosure-candidate['tube']))));assert valid==bool(candidate['valid'])
 assert maperr<1e-10 and tubeerr<1e-15
 # Exact stage derivative makes a coarser-held RK4 vs continuous-time map comparison,
 # not a proof that intermediate parameter values are in the finite enclosure.
 max_continuous_diff=0.
 for jf in np.linspace(.8,1.25,13):
  for tf in np.linspace(1,1.5,13):
   A,B,Ad,Bd=map_parts(c,jf,tf);M=np.zeros((7,7));M[:4,:4]=A;M[:4,4:]=B
   max_continuous_diff=max(max_continuous_diff,float(np.max(np.abs((expm(c['dt']*M)[:4,:4]-Ad)*np.array([1e-6,1e-6,1e-6,1e-6])[None,:]))))
 out={'status':'passed','finite_models':6,'candidates':len(L),'stage_constraint_checks':constraintchecks,'maximum_discrete_matrix_absolute_error':maperr,'maximum_tube_absolute_error_rad':tubeerr,'interior_parameter_maps_inspected':169,'maximum_continuous_vs_RK4_map_error_for_per_state_1e_minus6_scale':max_continuous_diff,'toolbox_availability':{k:int(v) for k,v in d['availability'].items()},'scope':'Independent Python stage recurrence and convolution agree with MATLAB library. No continuous-interval reachability proof, floating-point enclosure, or hardware guarantee. Intermediate grid trajectories are empirical stress tests.'};dump('actuator.json',out);print(out)
if __name__=='__main__':main()
