
def weight(masked_data, basin_no):
    '''
    input: masked basin data and basin id number 
    weights data according to gridbox size
    '''
    weight = mask_data2D(clat2D, basin_no)
    a = len(masked_data[:,0,0])
    weighted_data = np.zeros(a)
    for i in range(a):
        weighted_data[i] =(masked_data[i,:,:]*weight).sum()/(weight).sum()
    return weighted_data



def mask_data(data, basin_no):
    '''
    masks global data to give basin data 
    input: data and basin id number
    output: mask
    note: must have basinid downloaded (see Observational_data.py file) 
    '''
    a = len(data[:,0,0])
    mask_boolean = np.zeros(shape =(a,360,720))
    for i in range(360):
        for j in range(720):
            if basinid[i,j] == basin_no:
                mask_boolean[:,i,j] = 0
            else:
                mask_boolean[:,i,j] = 1
    masked_data = ma.masked_array(data, mask = mask_boolean)
    return masked_data

def mask_data2D(data, basin_no):
    '''
    input:
    '''
    mask_boolean = np.zeros(shape =(360,720))
    for i in range(360):
        for j in range(720):
            if basinid[i,j] == basin_no:
                mask_boolean[i,j] = 0
            else:
                mask_boolean[i,j] = 1
    masked_data = ma.masked_array(data, mask = mask_boolean)
    return masked_data
   
def continental_mask(data):
    '''
    Masks global data to give data only over land (consistent with GRUN runoff coverage) 
    input: data
    output: continental mask
    '''
    mask = np.zeros(shape =(len(data[:,0,0]),360,720))
    for i in range(360):
        for j in range(720):
            if Q[0,i,j] > -2:
                mask[:,i,j] = 0
            else:
                mask[:,i,j] = 1
    masked_data = ma.masked_array(data, mask = mask)
    return masked_data
  
  
def monthly_mean_w_array(masked_data, basin_no):
    '''
    this will weight the data according to gridbox size the plot msc
    '''
    data = weight(masked_data, basin_no)
    monthly_mean= np.zeros(12)
    for i in range(12):
        monthly_mean[i] = np.mean(data[i:144:12])
    return monthly_mean

# Read in mask
def mask_continent(data, cont_no):
    '''
    Takes 3D global data and masks  to give data for selected continent
    input: data, cont no. see key
    output: masked data 
    '''
    a = len(data[:,0,0])
    mask_boolean = np.zeros(shape =(a,360,720))
    for i in range(360):
        for j in range(720):
            if c_mask2[i,j] == cont_no:
                mask_boolean[:,i,j] = 0
            else:
                mask_boolean[:,i,j] = 1
    masked_data = ma.masked_array(data, mask = mask_boolean)
    return masked_data

def mask_continent2d(data, cont_no):
    '''
    Takes 2D global data and masks to give data for selected contient 
    input: data , continent number (See key) 
    output: masked data 
    '''
    mask_boolean = np.zeros(shape =(360,720))
    for i in range(360):
        for j in range(720):
            if c_mask2[i,j] == cont_no:
                mask_boolean[i,j] = 0
            else:
                mask_boolean[i,j] = 1
    masked_data = ma.masked_array(data, mask = mask_boolean)
    return masked_data



def mm_w_array(masked_data, basin_no):
    '''
    input: masked data, basin id number
    Produces monthly mean weighted array
    this will weight the data according to gridbox size 
    '''
    data = weight(masked_data, basin_no)
    monthly_mean= np.zeros(12)
    for i in range(12):
        monthly_mean[i] = np.mean(data[i::12])
    return monthly_mean
