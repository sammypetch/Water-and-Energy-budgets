
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
plt.style.use('seaborn')


xlab = np.arange(2002,2014,1/12) # xlabel = jan 2002- dec 2013

# Fig02 NET map

fig = plt.figure(figsize=(10,15))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.coastlines() 
ax.gridlines(draw_labels = True, linestyle = 'dashed', alpha = 0.5)
nlevs = 28
plt.contourf(mg_lonb, mg_latb, NET.mean(axis=0),nlevs,
      transform=ccrs.PlateCarree(),cmap = "RdYlBu')

plt.colorbar(label= "Wm$^{-2}$",
                orientation = 'horizontal', fraction = 0.09, pad= 0.04)
    
plt.savefig('NET_map.jpg', dpi=300)
plt.show()


# fig03 Water fluxes

plt.figure(figsize=(10,5))

plt.plot(xlab[:142], Popt[:], lw=1.5,linestyle = 'dashed', c = 'b', label = 'Optimised')
plt.plot(xlab[:142], Pobs[:], label = 'Observed', c = 'b', lw = 2, alpha=0.6, )
plt.fill_between(xlab[:142],  Pobs - Perror[:142],  Pobs + Perror[:142], alpha = 0.2, facecolor = 'k')

plt.plot(xlab[:142], Qopt[:],lw=1.5,linestyle = 'dashed', c = 'green', label = 'Optimised')
plt.plot(xlab[:142], Qobs, label = 'Observed', c = 'green', lw = 2 , alpha=0.6, )
plt.fill_between(xlab[:142],  Qobs - Qerror[:142],  Qobs + Qerror[:142], alpha = 0.2, facecolor = 'k')

plt.plot(xlab[:142], dSopt[:142], lw = 1.5 , linestyle = 'dashed', c = 'orange', label = 'Optimised')
plt.plot(xlab[:142], dSobs[0:142], label = 'Observed', c = 'gold', lw= 2, alpha = 0.6, )
plt.fill_between(xlab[:142], dSobs[:142]- Serror[:142],  dSobs[:142] + Serror[:142], alpha = 0.2, facecolor = 'k')

plt.plot(xlab[:142], LEopt[:], lw = 1.5, linestyle = 'dashed', c = 'r', label = 'Optimised')
plt.plot(xlab[:142], LEobs, label = 'Observed', c = 'r', lw = 2, alpha = 0.6, )
plt.fill_between(xlab[:142],  LEobs - LEerror[:142], LEobs + LEerror[:142], alpha = 0.2, facecolor = 'k')

plt.xlim(2002,2014)
plt.ylabel('Flux (mm day$^{-1}$')
plt.legend()
plt.show()


# fig04 Water storage 

PLEQb2= (Pb -LEb-Qb) # P - LE -Q
PLEQb = PLEQb2 - np.mean(PLEQb2) + np.mean(dSb) # match mean of GRACE 
gen_stor  = np.insert(PLEQb[0:143]*3.046, 0 , som_stor[0]) # FISw
gen_stor2  = np.insert(PLEQb2[0:143]*3.046, 0 , som_stor[0]) # FISwD (detrended) 

plt.figure(figsize=(10,5)) # FISw plot
plt.plot(xlab, GRACE_stom, color = 'orange', label = 'GRACE')
plt.plot(xlab, np.cumsum(gen_stor), color = '#8B3A62', label = 'FIS')
plt.plot(xlab, np.cumsum(gen_stor2), color = 'tab:red', ls = 'dashed' ,label = 'Unadjusted FIS', alpha=0.8)
plt.ylabel('Total Water Storage (cm)') 
plt.xlabel('Time')
plt.legend(loc = 'lower left')
plt.xlim(2002, 2014)
plt.savefig('GRACE_FISe.jpg', dpi=300)
plt.show()


PLEQ_opt = Popt- Qopt  - LEopt # P - LE -Q
opt_stor  = np.insert(PLEQ_opt_am[0:141]*3.046, 0 , GRACE_stom[0]) # create optimised storage 

plt.figure(figsize = (10,5)) # Optimisaed water storage plot
plt.plot(xlab[0:142], GRACE_stom, color = 'orange', label = 'GRACE', lw = 2.3)
plt.plot(xlab[0:142], np.cumsum(opt_stor), linestyle = 'dashed', dashes=(5, 7), color = 'b', label = 'Optimised Storage')
plt.ylabel('Total Water Storage (cm)')
water_difference = - GRACE_stom[0:142] + np.cumsum(opt_stor)
plt.plot(xlab, S_error*3.046, color = 'r', linewidth = 0.5, linestyle = 'dashdot', label = 'σ$_S$')
plt.plot(xlab, -S_error*3.046, color = 'r' , linewidth = 0.5, linestyle = 'dashdot')
plt.plot(xlab[0:142], water_difference_am, label = 'Difference', lw = 1.5)
plt.xlabel('Time')
plt.xlim(2002,2014)
plt.savefig('Optw.jpg', dpi = 300)
plt.show()


# fig06 Energy budget figures

plt.figure(figsize=(10,5))
plt.plot(xlab[0:142], DSRobs*28.9, c = C[0], label = 'DSR')  # convert aall figs to W/m2 from mm/day 
plt.plot(xlab[0:142], DSRopt*28.9, c = C[0] , linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (DSRobs[0:142] - DSRerror[0:142])*28.9, (DSRobs[0:142] + DSRerror[0:142])*28.9, alpha = 0.2, facecolor = C[0])  

plt.plot(xlab[0:142], DLRobs*28.9, c = C[1], label = 'DLR')  
plt.plot(xlab[0:142], DLRopt*28.9, c = C[1] , linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (DLRobs[0:142]- DLRerror[0:142])*28.9, (DLRobs[0:142] + DLRerror[0:142])*28.9, alpha = 0.2, facecolor = C[1])  

plt.plot(xlab[0:142], USWobs*28.9, c = C[5], label = 'USW')  
plt.plot(xlab[0:142], USWopt*28.9 ,c = C[5], linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (USWobs[0:142]- USWerror[0:142])*28.9, (USWobs[0:142] + USWerror[0:142])*28.9, alpha = 0.2, facecolor = C[5])  

plt.plot(xlab[0:142], ULWobs*28.9, c = C[3], label = 'ULW')  
plt.plot(xlab[0:142], ULWopt*28.9, c = C[3] , linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (ULWobs[0:142]- ULWerror[0:142])*28.9, (ULWobs[0:142] + ULWerror[0:142])*28.9, alpha = 0.2, facecolor = C[3])  

plt.plot(xlab[0:142], LEobs*28.9, c = C[6], label = 'LE')  
plt.plot(xlab[0:142], LEopt*28.9, c = C[6] , linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (LEobs[:142] - LEerror[0:142])*28.9, (LEobs[:142] + LEerror[0:142])*28.9,alpha = 0.2, facecolor = C[6])  

plt.plot(xlab[0:142], SHobs*28.9, c = C[2], label = 'SH')  
plt.plot(xlab[0:142], SHopt*28.9, c = C[2] , linestyle = 'dashed')    
plt.fill_between(xlab[0:142], (SHobs[0:142] - SHerror[0:142])*28.9, (SHobs[:142] + SHerror[0:142])*28.9, alpha = 0.2, facecolor = C[2])  

plt.plot(xlab[0:142], NETopt*28.9, c = 'k', label = 'NET',lw=1.5)  

plt.xlim(2002,2014)
plt.ylabel('Flux (Wm$^{-2}$)')
plt.xlabel('Time')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.show()




