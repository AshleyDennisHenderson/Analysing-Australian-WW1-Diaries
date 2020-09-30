###############################################################################################################################

## IMPORT PACKAGES

from date_conversions import *
import pandas as pd
import numpy as np
import random
import math
import os

###############################################################################################################################

def simulation_issue_1(dates, prob):

    """ Missing Years"""

    l = len(dates)  # How many dates we start with

    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))  # Choose altered dates

    sim_dates = dates

    sim_dates.iloc[r, 2] = 0

    return(sim_dates)

def simulation_issue_2(dates, prob):

    """ Missing Years"""

    l = len(dates)  # How many dates we start with

    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))  # Choose altered dates

    sim_dates = dates

    sim_dates.iloc[r, 1] = 0

    sim_dates.iloc[r, 2] = 0

    return(sim_dates)

def simulation_issue_3(dates, prob, prob2):

    """ Missing Years"""

    l = len(dates)  # How many dates we start with

    r = list(np.random.choice(range(l), size = math.floor(l*prob2), replace = False))  # Choose altered dates

    sim_dates = dates

    l2 = len(r)

    l3 = math.floor((prob/prob2)*l2)

    r1 = r[0:l3-1]  ## CHECK

    sim_dates.iloc[r1, 1] = 0

    sim_dates.iloc[r, 2] = 0

    return(sim_dates)
    
def simulation_issue_4(dates, prob):
    
    """ days randomly off by 1 less """
    
    l = len(dates)
    
    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))
    
    sim_dates = dates
    
    l2 = len(r)
    
    for i in range(l2):
        
        if sim_dates.iloc[r[i],0] == 1:
            
            sim_dates.iloc[r[i],0] == 31
            
            if sim_dates.iloc[r[i],1] == 1:
                
                sim_dates.iloc[r[i],1] == 12
                
                sim_dates.iloc[r[i],2] == sim_dates.iloc[r[i],2] - 1
                
            else:
                
                sim_dates.iloc[r[i],1] = sim_dates.iloc[r[i],1] - 1
            
        else:
            
            sim_dates.iloc[r[i],0] == sim_dates.iloc[r[i],0] - 1
            
    return(sim_dates)
    
def simulation_issue_5(dates, prob):
    
    """ days randomly off by 1 more """
    
    l = len(dates)
    
    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))
    
    sim_dates = dates
    
    l2 = len(r)
    
    for i in range(l2):
        
        if sim_dates.iloc[r[i],0] == 31:
            
            sim_dates.iloc[r[i],0] == 1
            
            if sim_dates.iloc[r[i],1] == 12:
                
                sim_dates.iloc[r[i],1] == 1
                
                sim_dates.iloc[r[i],2] == sim_dates.iloc[r[i],2] + 1
                
            else:
                
                sim_dates.iloc[r[i],1] = sim_dates.iloc[r[i],1] + 1
            
        else:
            
            sim_dates.iloc[r[i],0] == sim_dates.iloc[r[i],0] + 1
            
    return(sim_dates)
    
def simulation_issue_6(dates, prob):
    
    """ months randomly off by 1 less"""
    
    l = len(dates)
    
    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))
    
    sim_dates = dates
    
    l2 = len(r)
    
    for i in range(l2):
        
        if sim_dates.iloc[r[i],1] == 1:
            
            sim_dates.iloc[r[i],1] == 12
            
        else:
            
            sim_dates.iloc[r[i],1] == sim_dates.iloc[r[i],1] - 1
            
    return(sim_dates)
    
def simulation_issue_7(dates, prob):
    
    """ months randomly off by 1 more"""
    
    l = len(dates)
    
    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))
    
    sim_dates = dates
    
    l2 = len(r)
    
    for i in range(l2):
        
        if sim_dates.iloc[r[i],1] == 12:
            
            sim_dates.iloc[r[i],1] == 1
            
        else:
            
            sim_dates.iloc[r[i],1] == sim_dates.iloc[r[i],1] + 1
            
    return(sim_dates)
    
    
def simulation_issue_8(dates, prob, TD_F_path, TD_F_epoch_path, sd, ed, sy):
    
    """ random flashback/forward """
    
    l = len(dates)
    
    r = list(np.random.choice(range(l), size = math.floor(l*prob), replace = False))
    
    r.sort()
    
    extra_dates = dates.iloc[r,:]
    
    true_dates = dates.append(extra_dates)
    true_dates = true_dates.sort_values([2,1,0])
    true_dates = true_dates.reset_index(drop = True)
    
    true_date_list = true_dates.values.tolist()
    
    true_dates_epoch = convert_to_epoch(true_date_list, sy)
    
    true_dates_epoch = pd.DataFrame(true_dates_epoch)  # Convert list to pandas dataframe

    true_dates_epoch.to_csv(TD_F_epoch_path, index = False, header = False)  # Save to csv
    
    true_dates.to_csv(TD_F_path, index = False, header = False)  # Save to csv
    
    l2 = len(true_dates)
    
    d2 = true_dates
    
    for i in range(1,l2):
        
        if (d2.iloc[i,0] == d2.iloc[i-1,0]) & (d2.iloc[i,1] == d2.iloc[i-1,1]) & (d2.iloc[i,2] == d2.iloc[i-1,2]):
            
            new_date = np.random.randint(sd, high = ed+1)  # random day to change it to
            
            new_date = convert_to_expanded([new_date], sy)
            new_date = new_date[0]
            
            d2.iloc[i,0] = new_date[0]
            d2.iloc[i,1] = new_date[1]
            d2.iloc[i,2] = new_date[2]
            
    sim_dates = d2
            
    return(sim_dates)


def create_sim_date_set(TD_path, SD_path, issue, p_1, p_2, seed, TD_F_path, TD_F_epoch_path, sd, ed, sy):

    """ n = number of simulation of each probability, prob is vector of probabilities"""

    np.random.seed(seed)

    dates = pd.read_csv(TD_path, header = None)  # Load date set

    if issue == 1:

        sim_dates = simulation_issue_1(dates, p_1)

    if issue == 2:

        sim_dates = simulation_issue_2(dates, p_1)

    if issue == 3:

        sim_dates = simulation_issue_3(dates, p_1, p_2)
        
    if issue == 4:
        
        sim_dates = simulation_issue_4(dates, p_1)
        
    if issue == 5:
        
        sim_dates = simulation_issue_5(dates, p_1)
        
    if issue == 6:
        
        sim_dates = simulation_issue_6(dates, p_1)
        
    if issue == 7:
        
        sim_dates = simulation_issue_7(dates, p_1)
        
    if issue == 8:
        
        sim_dates = simulation_issue_8(dates, p_1, TD_F_path, TD_F_epoch_path, sd, ed, sy)

    sim_dates.to_csv(SD_path, index = False, header = False)



