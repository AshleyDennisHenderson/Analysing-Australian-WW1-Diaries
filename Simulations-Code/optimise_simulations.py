###############################################################################################################################

## IMPORT PACKAGES

from date_conversions import *
import pandas as pd
import numpy as np
from optimise_dates2 import optimise_dates2

###############################################################################################################################

def create_opt_date_set(SD_path, OD_path, OD_epoch_path, sd, start_year, alpha, beta, gamma, delta, omega):

    sim_dates = pd.read_csv(SD_path, header = None)  # Load sim date set

    sim_I = 1*(sim_dates!=0)  # Create indicator matrix

    (dates_opt, opt) = optimise_dates2(sim_dates, sim_I, sd, start_year, alpha, beta, gamma, delta, omega)  # Optimise
    
    if (opt > -1):
        
        dates_opt = pd.DataFrame(dates_opt, dtype = 'int')
       
        dates_opt.to_csv(OD_path, index = False, header = False)
       
        opt_res_list = dates_opt.values.tolist()
       
        opt_res = convert_to_epoch(opt_res_list, start_year)
       
        opt_res = pd.DataFrame(opt_res)
       
        opt_res.to_csv(OD_epoch_path, index = False, header = False)
    
    return(opt)

###############################################################################################################################

