from netCDF4 import Dataset    
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma


# Read in data files

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
SH_errorNEWA = NEWS_error_data.variables['SHerror_obs_rate'][:]

lat_rad = b_lat*np.pi/180 # convert to radian
cos_lat = np.cos(lat_rad)
lons2D, clat2D = np.meshgrid(b_lon,cos_lat)

# LE data
LE_fn = 'LE.RS_METEO.EBC-ALL.MLM-ALL.METEO-ALL.720_360.nc' # filename 
letdat = Dataset(LE_fn)

