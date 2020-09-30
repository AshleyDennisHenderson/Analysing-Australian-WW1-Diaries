###############################################################################################################################

## IMPORT PACKAGES

from date_conversions import *
import pandas as pd
import numpy as np

###############################################################################################################################

def get_sim_results(TD_epoch_path, OD_epoch_path):

    true_dates = pd.read_csv(TD_epoch_path, header = None)

    opt_dates = pd.read_csv(OD_epoch_path, header = None)

    correct = 1*(true_dates == opt_dates)

    num_correct = correct.sum()

    num_correct = int(num_correct)

    l = len(true_dates)

    prop = num_correct/l

    num_days = abs(true_dates - opt_dates)

    sum_num_days = num_days.sum()

    sum_num_days = int(sum_num_days)

    av_num_days = sum_num_days/l

    return([prop, av_num_days])

    
