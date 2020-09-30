###############################################################################################################################

## IMPORT PACKAGES

import os
from create_date_set import *
from create_simulation_data import *
from optimise_simulations import *
from sim_results import *
from multiprocessing import Process
import time


###############################################################################################################################

def run_simulation(spacing = 'E', p_true = 1, seed = 1, start_year = 2000, start_date = [[1, 1, 2001]], end_date = [[31, 12, 2001]], issue = 1, p_1 = 0.5, p_2 = 0, alpha = 1, beta = 1, gamma = 1, delta = 1, omega = 1):


    """
    This function takes in parameters and runs the corresponding simulation.

    Parameters
    ----------
    spacing : chr ('R' or 'E')
        This determines whether the initial true data set has randomly ('R') or
        evenly ('E') spaced days. It has a default vaule of 'E'.
    p_true : int
        For spacing = 'E' this keeps every p_true day, i.e. if p_true = 2 it keeps
        every second day and if p_true = 3 it keeps every third day.
        For spacing = 'R' this is the proportion of dates kept in the true date set.
        The default value is 1 (i.e. for every day).
    seed : ?
        This is the seed for the random number generator (for when random days are
        kept in the true date set). The default value is 1. 
    start_year : int
        The year for which we want to know the number of days since. The default 
        value is 2000.
    start_date : list (int)
        T
    end_date :
        T
    issue : int
        Number relating to what issue we are simulating. The default value is 1.
            1 = missing years only
            2 = missing months and years (pairs only)
            3 = missing months and years
    p_1 : float
        Proportion of dates altered by the issue (1st parameter). The default is 0.5.
    p_2 : float
        Proportion of dates altered by the issue (2nd parameter). The default is 0.
    alpha, beta, gamma, delta : float
        Optimisation parameters. Default is 1.
    

    Output
    ------
    ...

    Author
    ------
    Ashley Dennis-Henderson
    ashley.dennis-henderson@adelaide.edu.au"""

    seed2 = seed + int(p_1*100) + int(p_2*100)

    TD_dir = 'True_Date_Sets'  # Directory for True Date Sets
    SD_dir = 'Sim_Date_Sets'  # Directory for Simulated Date Sets
    OD_dir = 'Opt_Date_Sets'  # Directory for Optimised Date Sets

    sd = convert_to_epoch(start_date, start_year)
    ed = convert_to_epoch(end_date, start_year)

    sd = sd[0]
    ed = ed[0]

    filename_1 = spacing + '_' + str(p_true) + '_' + str(seed) + '_' + str(start_year) + '_' + str(sd) + '_' + str(ed)
    filename_2 = str(issue) + '_' + str(p_1) + '_' + str(p_2) + '_' + str(seed2)
    filename_3 = str(alpha) + '_' + str(beta) + '_' + str(gamma) + '_' + str(delta) + '_' + str(omega)

    TD_path = TD_dir + '/True_Date_Set_' + filename_1 + '.csv'  # True date set filename
    TD_epoch_path = TD_dir + '/True_Date_Set_Epoch_' + filename_1 + '.csv'  
    TD_F_path = TD_dir + '/True_Date_Set_F_' + filename_1 + '_' + filename_2 + '.csv'  # True date set filename
    TD_F_epoch_path = TD_dir + '/True_Date_Set_Epoch_F_' + filename_1 + '_' + filename_2 + '.csv'  
    SD_path = SD_dir + '/Sim_Date_Set_' + filename_1 + '_' + filename_2 + '.csv'  # Sim date set filename
    OD_path = OD_dir + '/Opt_Date_Set_' + filename_1 + '_' + filename_2 + '_' + filename_3 + '.csv'  # Opt date set filename
    OD_epoch_path = OD_dir + '/Opt_Date_Set_Epoch_' + filename_1 + '_' + filename_2 + '_' + filename_3 + '.csv'  # Opt date set filename

    column_names = ["spacing", "p_true", "seed", "start_year", "start_date", "end_date", "issue", "p_1", "p_2", "seed_2", "alpha", "beta", "gamma", "delta", "omega", "accuracy", "av_num_days", "opt"]

    ## CHECK INPUTS

    if not (spacing == 'R' or spacing == 'E'):

        raise ValueError("Spacing must be either 'R' for random, or 'E' for evenly spaced") 

    if not (type(p_true) == float or type(p_true) == int): 

        raise ValueError("p_true must be a number in the range [0,1]")

    if not (p_true <=1 and p_true >= 0):

        raise ValueError("p_true must be a number in the range [0,1]")

    if not (type(seed) == int):

        raise ValueError("seed must be an integer")

    if not (type(start_year) == int):

        raise ValueError("start_year must be an integer")

    if not (type(issue) == int):

        raise ValueError("issue must be an integer")

    if not (type(p_1) == float or type(p_1) == int):

        raise ValueError("p_1 must be a numerical value in [0,1]")

    if not (p_1 <= 1 and p_1 >= 0):

        raise ValueError("p_1 must be a numerical value in [0,1]")

    if not (type(p_2) == float or type(p_2) == int):

        raise ValueError("p_2 must be a numerical value in [0,1]")

    if not (p_2 <= 1 and p_2 >= 0):

        raise ValueError("p_2 must be a numerical value in [0,1]")

    if not (type(alpha) == float or type(alpha) == int):

        raise ValueError("alpha must be a numerical value")

    if not (type(beta) == float or type(beta) == int):

        raise ValueError("beta must be a numerical value")
    
    if not (type(gamma) == float or type(gamma) == int):

        raise ValueError("gamma must be a numerical value")
    
    if not (type(delta) == float or type(delta) == int):

        raise ValueError("delta must be a numerical value")
    
    #df = pd.read_csv('Simulation_Results.csv')

    if not os.path.exists(OD_path):  # If this simulation hasn't been run

        ## CHECK IF TRUE DATE SET EXISTS
        
        #if not ((df['p_true'] == p_true) & (df['seed'] == seed) & (df['issue'] == issue) & (df['p_1'] == p_1) & (df['p_2'] == p_2) & (df['alpha'] == alpha) & (df['beta'] == beta) & (df['gamma'] == gamma) & (df['delta'] == delta)).any():  # If simulation hasnt been run

        if not os.path.exists(TD_dir):  # If no directory exists for the true date sets

            os.makedirs(TD_dir)  # Create directory

        if not os.path.exists(TD_path):  # If true date set doesn't exist

            create_true_date_set(TD_path, TD_epoch_path, spacing, p_true, seed, start_year, start_date, end_date) # Create true date set

            # This creates date set and saves to right place

        # CHECK IF SIM DATE SET EXISTS

        if not os.path.exists(SD_dir):  # If no directory exists for the sim date sets

            os.makedirs(SD_dir)  # Create directory

        if not os.path.exists(SD_path):  # If sim date set doesn't exists

            create_sim_date_set(TD_path, SD_path, issue, p_1, p_2, seed2, TD_F_path, TD_F_epoch_path, sd, ed, start_year)  # Create sim date set

            # Creates it and sabes to right place

        if not os.path.exists(OD_dir):  # If no dir exists for opt dates

            os.makedirs(OD_dir)  # Create directory
            
        #action_process = Process(target = 
        opt = create_opt_date_set(SD_path, OD_path, OD_epoch_path, sd, start_year, alpha, beta, gamma, delta, omega)#)
        
        #action_process.start()
        #action_process.join(timeout = 90)
        
       # action_process.terminate()

        if not os.path.exists(OD_epoch_path):
            
            print(OD_epoch_path)

        if os.path.exists(OD_epoch_path):
            
            if issue == 8:
                
                results = get_sim_results(TD_F_epoch_path, OD_epoch_path)
                
            else:

                results = get_sim_results(TD_epoch_path, OD_epoch_path)

            if not os.path.exists('Simulation_Results.csv'):

                df = pd.DataFrame(columns = column_names)

                df.to_csv('Simulation_Results.csv', index = False)

            df_entry = pd.DataFrame([[spacing, p_true, seed, start_year, sd, ed, issue, p_1, p_2, seed2, alpha, beta, gamma, delta, omega, results[0], results[1], opt]], columns = column_names)

            df_entry.to_csv('Simulation_Results.csv', index = False, mode = 'a', header = False)

        
###############################################################################################################################

## RUN SIMULATIONS

spacing = 'R'

p_true_vec = [0.1, 0.3, 0.5, 0.7, 0.9]

seed_vec = range(1,101)

issue_vec = [8]

start_year = 2000
start_date = [[1, 1, 2001]]
end_date = [[31, 12, 2001]] 

p_1_vec = [0.25, 0.5, 0.75, 1]
p_2_vec = [1]#[0.5, 0.75, 1]
param_vec = [1, 0.25, 0.5, 0.75, 25, 50, 75, 100]



for i1 in range(len(issue_vec)):  # For every issue

    issue = issue_vec[i1]  # Set issue number

    for i2 in range(len(p_true_vec)):  # For every p_true

        p_true = p_true_vec[i2]  # Set p_true

        for i3 in range(100):  # For every random number seed

            seed = seed_vec[i3]  # Set seed

            for i4 in range(len(p_1_vec)):  # For every p_1

                p_1 = p_1_vec[i4]  # Set p_1

                for i5 in range(len(p_2_vec)):  # For every p_2

                    p_2 = p_2_vec[i5]  # Set p_2
                    
                    if p_2 > p_1:

                        for i6 in range(5):  # For each parameter
    
                            if i6 == 0:
    
                                for i7 in range(len(param_vec)):  # For each parameter value
    
                                    alpha = param_vec[i7]
                                    beta = 1
                                    gamma = 1
                                    delta = 1
                                    omega = 1
    
                                    run_simulation(spacing, p_true, seed, start_year, start_date, end_date, issue, p_1, p_2, alpha, beta, gamma, delta, omega)
    
                            if i6 == 1:
    
                                for i7 in range(len(param_vec)):  # For each parameter value
    
                                    alpha = 1
                                    beta = param_vec[i7]
                                    gamma = 1
                                    delta = 1
                                    omega = 1
    
                                    run_simulation(spacing, p_true, seed, start_year, start_date, end_date, issue, p_1, p_2, alpha, beta, gamma, delta, omega)
    
                            if i6 == 2:
    
                                for i7 in range(len(param_vec)):  # For each parameter value
    
                                    alpha = 1
                                    beta = 1
                                    gamma = param_vec[i7]
                                    delta = 1
                                    omega = 1
    
                                    run_simulation(spacing, p_true, seed, start_year, start_date, end_date, issue, p_1, p_2, alpha, beta, gamma, delta, omega)
    
                            if i6 == 3:
    
                                for i7 in range(len(param_vec)):  # For each parameter value
    
                                    alpha = 1
                                    beta = 1
                                    gamma = 1
                                    delta = param_vec[i7]
                                    omega = 1
    
                                    run_simulation(spacing, p_true, seed, start_year, start_date, end_date, issue, p_1, p_2, alpha, beta, gamma, delta, omega)                              
    
    
                            if i6 == 4:
    
                                for i7 in range(len(param_vec)):  # For each parameter value
    
                                    alpha = 1
                                    beta = 1
                                    gamma = 1
                                    delta = 1
                                    omega = param_vec[i7]
    
                                    run_simulation(spacing, p_true, seed, start_year, start_date, end_date, issue, p_1, p_2, alpha, beta, gamma, delta, omega)                              

                                
                


