from netCDF4 import Dataset    
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma


# Read in data files

# Read in mask data
basin_fn = 'basins.nc'
basin = Dataset(basin_fn)

basinid = basin.variables['basinid'][:] 
b_lat = basin.variables['latitude'][:] # 90- -90 0.5 degree
b_lon = basin.variables['longitude'][:] # -180-180
mg_lonb, mg_latb = np.meshgrid(b_lon, b_lat)

b =  np.meshgrid(b_lon, b_lat)

lat_rad = b_lat*np.pi/180 # convert to radian
cos_lat = np.cos(lat_rad)
lons2D, clat2D = np.meshgrid(b_lon,cos_lat)    
    


# Latent heat data (LE) 
LE_fn = 'LE.RS_METEO.EBC-ALL.MLM-ALL.METEO-ALL.720_360.nc' # filename 
letdat = Dataset(LE_fn)

# Sensible heat data (SH)
SH_fn= 'H.RS_METEO.EBC-ALL.MLM-ALL.METEO-ALL.720_360.monthly.nc'
SH01_data = Dataset(SH_fn)
  
# Runoff data (Q)
runoff_fn = 'GRUN_v1_GSWP3_WGS84_05_1902_2014.nc'
runoff_data = Dataset(runoff_fn)
runoff = runoff_data.variables['Runoff'][:]

# change until days since 2001-01-01 to match storage data
runoff = runoff[1188:,:,:]

# correct lat and lon data to match mask 
Q = runoff[:,::-1,:]
    

# Precipitation data (P)
precip_fn = 'precip.mon.mean.nc'
precip_data = Dataset(precip_fn)
precip = precip_data.variables['precip'][:] # mm /day
precip25res = precip[264:,:,:] # convert to days since 2001 - 01 -01 
precip = precip[264:,:,:]

# make precipitation data the right size 
p2 = np.repeat(precip, 5, axis = 1)
p3 = np.repeat(p2, 5, axis = 2)
precip = p3 

# correct precipitation lat and lon
precip2 = precip[:,::-1,:]
a1 = precip2[:,:,0:360]
b2 = precip2[:,:,360:720]
c3 = np.concatenate((b2,a1), axis = 2)

P = c3 
# mask to give data over land only 
P_cont = continental_mask(P)

# interpolated storage data GRACE
storage_filled_fn = 'GRACE_2001_2020_land_mthly_interp_copy.nc'
storage_filled_data = Dataset(storage_filled_fn)
stor_fill_time = storage_filled_data.variables['time'][:]
stor_fill = storage_filled_data.variables['storage'][:]
S_fill = stor_fill[:,::-1,:]

# calculate dS from S
stor_fill02 = S_fill[11:240,:,:]

dS = np.zeros(shape = (227, 360, 720)) # begins jan 2002

for i in range(225):
    dS[i,:,:] = (stor_fill02[i+2,:,:] - stor_fill02[i,:,:])/2
# connvert dS into mm/day from cm/month
dS=dS/ md2cm # in mm/day 
dS = ma.masked_greater(dS, 999) 

# CERES data USW, ULW, DSR,DLR
ceres_filename = 'CERES_EBAF_Ed4.1_Subset_200003-202006.nc'
ceres_data = Dataset(ceres_filename)

# separate variables 
srf_net_tot = data.variables['sfc_net_tot_all_mon'][:]
srf_down_lw = data.variables['sfc_lw_down_all_mon']
srf_up_lw = data.variables['sfc_lw_up_all_mon']
srf_down_sw = data.variables['sfc_sw_down_all_mon']
srf_up_sw = data.variables['sfc_sw_up_all_mon']

# function to match CERES data to the same as basin mask 
def match_mask_dims(data):
    # make 0.5x0.5 grids (360x720)
    data1 = np.repeat(data, 2, axis = 1)
    data2 = np.repeat(data1, 2, axis = 2)
    
    # flip lat
    data3 = data2[:,::-1,:]
    
    # correct for lon
    a1 = data3[:,:,0:360]
    a2 = data3[:,:,360:720]
    output = np.concatenate((a2,a1), axis = 2)
    return output

# create global data o same dimensions as mask  
DSR_global = match_mask_dims(srf_down_sw) 
DLR_global = match_mask_dims(srf_down_lw)
USW_global  = match_mask_dims(srf_up_sw) 
ULW_global = match_mask_dims(srf_up_lw) 
Rn_global = match_mask_dims(srf_net_tot)  

# convert to mm/day from Wm-2
DSR = DSR_global/28.9 
DLR = DLR_global/28.9
USW = USW_global/28.6
ULW = ULW_global/28.9


# NEWS uncertainties 
NEWS_error_fn = 'NEWS_WEB_MCLIM.1.0.copy.nc4'
NEWS_error_data = Dataset(NEWS_error_fn)


# Continental uncertainties in mm/day
P_errorNEWS = NEWS_error_data.variables['Perror_obs_rate'][:]
Q_errorNEWS = NEWS_error_data.variables['Qerror_obs_rate'][:]
LE_errorNEWS = NEWS_error_data.variables['Eerror_obs_rate'][:]

DLR_errorNEWS = NEWS_error_data.variables['DLRerror_obs_rate'][:]
DSR_errorNEWS = NEWS_error_data.variables['DSRerror_obs_rate'][:]
ULW_errorNEWS = NEWS_error_data.variables['ULWerror_obs_rate'][:]
USW_errorNEWS = NEWS_error_data.variables['USWCerror_obs_rate'][:]
SH_errorNEWS = NEWS_error_data.variables['SHerror_obs_rate'][:]
