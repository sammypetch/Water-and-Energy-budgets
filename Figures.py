
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use('seaborn')

# Fig02 NET map


# fig03 Water fluxes

# fig04 Water storage 



PLEQb2= (Pb -LEb-Qb) # P - LE -Q
PLEQb = PLEQb2 - np.mean(PLEQb2) +np.mean(dSb) # match mean of GRACE 
       
gen_stor  = np.insert(PLEQb[0:143]*3.046, 0 , som_stor[0])
gen_stor2  = np.insert(PLEQb2[0:143]*3.046, 0 , som_stor[0])

plt.figure(figsize=(10,5))
plt.plot(xlab, som_stor, color = 'orange', label = 'GRACE')
plt.plot(xlab, np.cumsum(gen_stor), color = '#8B3A62', label = 'FIS')
plt.plot(xlab, np.cumsum(gen_stor2), color = 'tab:red',ls='dashed' ,label = 'Unadjusted FIS', alpha=0.8)
plt.ylabel('Total Water Storage (cm)')
plt.xlabel('Time')
plt.legend(loc='lower left')
plt.xlim(2002,2014)
plt.savefig('GRACE_FISe.jpg', dpi=300)
plt.show()



# fig06 Energy budget figures

# fig07  energy adjustments 



