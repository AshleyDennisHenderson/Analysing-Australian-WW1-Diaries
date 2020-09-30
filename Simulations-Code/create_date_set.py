###############################################################################################################################

## IMPORT PACKAGES

from date_conversions import *
import pandas as pd
import numpy as np
import os
import random
import math

###############################################################################################################################

def create_true_date_set(save_path, save_path_epoch, spacing = 'R', p_true = 0.5, seed = 1, start_year = 2000, start_date = [[1, 1, 2001]], end_date = [[31, 12, 2001]]):

    """
    This function takes creates a date set based on the given parameters.
    
	
    Parameters
    ----------
    start_year : int
        The year for which we want to know the number of days since. The default 
        value is 2000.
    start_date : list (int)
        T
    end_date :
        T
    set_type : 
    seed : int
        Seed for the random number generator
    percent : int
        Percentage of days to be chosen
    filename : str
        string for filename
    

    Output
    ------

    Author
    ------
    Ashley Dennis-Henderson
    ashley.dennis-henderson@adelaide.edu.au"""

###############################################################################################################################

    ## INITIAL SET UP

    ## RUN TESTS ON INPUTS
    
    np.random.seed(seed)  # Set seed for random numbers

    Start_Date_Epoch = convert_to_epoch(start_date, start_year)  # Convert start date into epoch form

    End_Date_Epoch = convert_to_epoch(end_date, start_year)  # Convert end date into epoch form

    x = list(range(Start_Date_Epoch[0], End_Date_Epoch[0] + 1))  # List containing every day of date range in epoch form

    x_length = len(x)  # How many possible days in our date range

    if spacing == 'R':

        x_subset = list(np.random.choice(x, size = math.floor(x_length*(p_true)), replace = False))  # Randomly choose % of dates (without replacement)

        x_subset.sort()  # Sort the dates into order

    if spacing == 'E':

        x_subset == x[::p_true]

    date_set = convert_to_expanded(x_subset, start_year)  # Convert dates to expanded form

    date_set = pd.DataFrame(date_set)  # Convert list to pandas dataframe

    date_set.to_csv(save_path, index = False, header = False)  # Save to csv

    x_subset = pd.DataFrame(x_subset)  # Convert to pandas dataframe

    x_subset.to_csv(save_path_epoch, index = False, header = False)

###############################################################################################################################

