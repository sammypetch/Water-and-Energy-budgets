
def optimisation(month):
    '''
    water and energy optimisation
    input kth month to find optimised fluxes for month k
    months 1 to 144
    
    must pre define basin fluxes and basin uncertainites in form Perror, Pobs etc
    '''
    i = month
    # smooth error 
    S = [Perror[i], Qerror[i], LEerror[i], Serror[i],
         DSRerror[i],DLRerror[i], USWerror[i], ULWerror[i],
         SHerror[i], Eerror[i]]
    
    S = np.square(S)
    
    S_obs = np.diag(S)
    
    # observation vector 
    F =[Pobs[i], Qobs[i], LEobs[i], D[i], DSRobs[i], DLRobs[i],
        USWobs[i], ULWobs[i], SHobs[i], E[i]]
    # budget constraint
    AT= np.array([1,-1,-1,-1, 0, 0, 0, 0, 0, 0])
    A = np.reshape(AT,(1,10))
    
    BT= np.array([0,0,-1,0, 1, 1, -1, -1, -1, -1])
    B = np.reshape(BT,(1,10))

    S_Robs_inv = np.linalg.inv(S_obs)

    alpha1 = S_Robs_inv@F
    alpha2 = np.append(alpha1,0)
    alpha = np.append(alpha2,0)

    x2 = np.append(A,0)
    x2 = np.append(x2,0).reshape(12,1)
    
    x3 =np.append(B,0)
    x3 =np.append(x3,0).reshape(12,1)

    X = np.vstack((S_Robs_inv,A))
    X = np.vstack((X,B))
    
    X = np.hstack((X,x2))
    X = np.hstack((X,x3))

    X_trans = np.transpose(X)
    beta = (np.linalg.inv((X@X_trans))@X_trans)@alpha
    return beta, beta[3], beta[9]

b = # USER DEFINE BASIN NUMBER

Pobs, Qobs, LEobs, dSobs, DSRobs, DLRobs, USWobs ,ULWobs, SHobs , NETobs = basin_fluxes(b) # basin observed fluxes
GRACE_stom =  stor_stom(b) # start of month GRACE water storage  data 
FISeD =  calculate_FISeD(b) # Flux inferred energy storage 

md2cm = 3.046 # mm/day to cm/month conversion constant
n = len(Pobs) # number of months of observations  
  
  
# initialise with dS1 and dE1
D[0] = (GRACE_stom[1] - GRACE_stom[0])/md2cm # convert unit 
E[0] = (FISeD[1] - FISed[0])


# Loop over months to solve for NET and dS to use in D and E array 
for i in range(n-2):
    NETopt = np.append(NETopt, optimisation(i)[2])
    dSopt = np.append(dSopt, optimisation(i)[1])
  
    # start at 1 since we initialised already 
    D[i+1] = (GRACE_stom[i+2] - GRACE_stom[0])/md2cm - sum(dSopt[0:i+1])
    E[i+1] = (FISeD[i+2] - FISeD[0])/md2cm- sum(NETopt[0:i+1])

# loop over n months (period can be changed according to length of obs 

for i in range(n):    
    opt_sol = np.append(opt_sol, optimisation(i)[0])

# reshape array into the differnt fluxes, note: last 2 columns are tehe lagrange multipliers    
basin_opt_sol = opt_sol.reshape(n,12)

# Optimised fluxes,  units:  mm/day
Popt = basin_opt_sol[:,0] # precipitation
Qopt = basin_opt_sol[:,1] # runoff 
LEopt = basin_opt_sol[:,2] # latent heat
dSopt = basin_opt_sol[:,3] # storage change
DSRopt = basin_opt_sol[:,4] # downwards shortwave
DLRopt = basin_opt_sol[:,5] # downwards longwave
USWopt = basin_opt_sol[:,6] # upwards shortwave
ULWopt = basin_opt_sol[:,7] # upwards longwave
SHopt = basin_opt_sol:,8] # sensible heat 
NETopt = basin_opt_sol[:,9] # NET 

