
def basin_error(C, B, cont_flux, cont_error):
    '''
    calculates basin uncertainty by downscaling continental uncertainties using assosiated areas.
    
    C = continent number, see key 1 to 4
    NA = 1, SA = 2 ,EA = 3, AF = 4
    
    B = basin number
    enter basin id number from 1-28
    
    cont_flux = average continental flux taken from NEWS
    cont_error = average continetal flux error taken from NEWS 

    '''
    
    C_area =  Area_cont[C-1] # continent area
    B_area = Basin_areas[B-1] # basin area 
     
    error = np.zeros(12)
    for i in range(12):
        error[i] = np.sqrt((basin_flux[i]/cont_flux[i])/(B_area/C_area))*cont_error[i] 
    return error



Area_name = ['North America', 'South America', 'Eurasia', 'Africa']
Area_cont =[24030089, 17737690, 53234055, 29903956] # area in km^2

Basin_areas = [5853804,3826122,3698802.75,3202958.75,2902864.5,2661391.75 
,2582221,2570130.5,2417937.25,2240018.75,1988755.75,1818799.375,1794242.5
,1712738.25,1628404.5,1571536,1463314.75,1266641.75,1143101.125,
1070229.875,1047385.687,1039361.750,1031512.062,977516.437,967340.562,
943577.187,893627.312]


