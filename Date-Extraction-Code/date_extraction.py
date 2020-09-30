## Import Packages ----

import string
import errors
import pandas as pd
import sys
sys.path.append('D:\date-extraction\Regular Expressions')
import date_conversions
from date_1 import date_form_1 as df1
from date_2 import date_form_2 as df2
from date_3 import date_form_3 as df3
from date_4 import date_form_4 as df4
from date_5 import date_form_5 as df5
from date_6 import date_form_6 as df6
from date_7 import date_form_7 as df7
from date_8 import date_form_8 as df8
from date_9 import date_form_9 as df9
from date_10 import date_form_10 as df10
from date_11 import date_form_11 as df11
from date_12 import date_form_12 as df12
from date_13 import date_form_13 as df13
from date_14 import date_form_14 as df14
from date_15 import date_form_15 as df15
from date_16 import date_form_16 as df16
from optimise_dates import optimise_dates
from estimate_dates import estimate_dates


def extract_dates(text, date_form = "raw", languages = ['en'], optimise = False, date_type = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], start_date = [1,1,2000], end_date = [31,12,2000], year_prefix = '20', start_year = 2000, opto_param = [1,1,1,1,1]):

    """
    This function takes a string and returns two pandas data frames. The
    first data frame contains the dates within the string, with the format
    of these dependent on the input parameters. The second data frame contains
    the location of the dates within the text. 

    Parameters
   ----------
    text : str
        The string we wish to parse for dates
    date_form : str (raw or list)
        Whether we want the dates to be given in the raw form from the string,
        or as a list ([dd, mm, yyyy]). The two input options are "raw" and
        "list", with the default being "raw".
    languages: list
        What languages to consider. Options: 'en' = English, 'fr' = French,
        'de' = German. Default is ['en']
    optimise : bool
        Whether we wish to optimise the dates so that they are in order (i.e.
        remove 'flashbacks', etc.). The two input options are False and True, 
        with the default being False.
    date_type : list
        List of date forms to be used, i.e. [1,2,4]. Note, the list may only
        include the integers 1,...,6 and the default is [1,2,3,4,5,6] (i.e. all
        date forms).
    start_date : ?
        A known (or estimated) start date for the text. This is necessary for
        optimisation.
    year_prefix : str
        A string of length 2 which gives the ? for the date, i.e. for dates known
        to be between 2010 and 2020 the prefix would be '20'. The default is '20'.
    start_year: int
        ?
    

    Output
    ------
    date_list : list
        A list of dates with qualities based on the given parameters.


    Author
    ------
    Ashley Dennis-Henderson
    ashley.dennis-henderson@adelaide.edu.au
    """
    

    
    # DATE TYPE

    location = True

    
    if date_type == "all":

        date_type = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]


    ## Extract Dates from Text ---- 

    complete_date_list = []  # Create empty list to store dates
    complete_locations_list = []  # Create empty list to store locations

    if 1 in date_type:  # If we want dates of form 1

        (date_list, locations_list, text) = df1(text, date_form, languages, year_prefix)  # Get dates of form 1
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 2 in date_type:  # If we want dates of form 2

        (date_list, locations_list, text) = df2(text, date_form, languages, year_prefix)  # Get dates of form 2

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 3 in date_type:  # If we want dates of form 3

        (date_list, locations_list, text) = df3(text, date_form, languages, year_prefix)  # Get dates of form 3

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list 

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 4 in date_type:  # If we want dates of form 4

        (date_list, locations_list, text) = df4(text, date_form, languages, year_prefix)  # Get dates of form 4

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list


    if 5 in date_type:  # If we want dates of form 5

        (date_list, locations_list, text) = df5(text, date_form, languages, year_prefix)  # Get dates of form 5

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 6 in date_type:  # If we want dates of form 6

        (date_list, locations_list, text) = df6(text, date_form, languages, year_prefix)  # Get dates of form 6

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list


    if 9 in date_type:  # If we want dates of form 9

        (date_list, locations_list, text) = df9(text, date_form, languages, year_prefix)  # Get dates of form 9

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 10 in date_type:  # If we want dates of form 10

        (date_list, locations_list, text) = df10(text, date_form, languages, year_prefix)  # Get dates of form 10
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list
        

    if 7 in date_type:  # If we want dates of form 7

        (date_list, locations_list, text) = df7(text, date_form, languages, year_prefix)  # Get dates of form 7

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 8 in date_type:  # If we want dates of form 8

        (date_list, locations_list, text) = df8(text, date_form, languages, year_prefix)  # Get dates of form 8

        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list



    if 11 in date_type:  # If we want dates of form 1

        (date_list, locations_list, text) = df11(text, date_form, languages, year_prefix)  # Get dates of form 11
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 12 in date_type:  # If we want dates of form 12

        (date_list, locations_list, text) = df12(text, date_form, languages, year_prefix)  # Get dates of form 12
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 13 in date_type:  # If we want dates of form 13

        (date_list, locations_list, text) = df13(text, date_form, languages, year_prefix)  # Get dates of form 13
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 14 in date_type:  # If we want dates of form 14

        (date_list, locations_list, text) = df14(text, date_form, languages, year_prefix)  # Get dates of form 14
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 15 in date_type:  # If we want dates of form 15

        (date_list, locations_list, text) = df15(text, date_form, languages, year_prefix)  # Get dates of form 15
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    if 16 in date_type:  # If we want dates of form 16

        (date_list, locations_list, text) = df16(text, date_form, languages, year_prefix)  # Get dates of form 16
        
        complete_date_list = complete_date_list + date_list  # Add dates to the complete list

        complete_locations_list = complete_locations_list + locations_list  # Add locations to the complete list

    

    ## Order Date List ----

    if complete_date_list == []:  # no dates extracted

        r2 = pd.DataFrame(complete_date_list)
        l2 = pd.DataFrame(complete_date_list)
        opt = -10
        

    else:
        
        sorted_index = sorted(range(len(complete_locations_list)),key=lambda x:complete_locations_list[x])
        final_date_list = [complete_date_list[i] for i in sorted_index ]
        final_locations_list = [complete_locations_list[i] for i in sorted_index ]

        #final_date_list = sorted(complete_date_list)  # Ordered based on location within text

        l = len(final_date_list)  # Number of dates found

        dl = pd.DataFrame(final_date_list)


        ## Optimise Date List ----

        sd = 372*(int(start_date[2])-start_year)+31*(int(start_date[1])-1)+int(start_date[0])-1
        ed = 372*(int(end_date[2])-start_year)+31*(int(end_date[1])-1)+int(end_date[0])-1

        if optimise == True:

            k_list = 1*(dl!=0)

            alpha = opto_param[0]
            beta = opto_param[1]
            gamma = opto_param[2]
            delta = opto_param[3]
            omega = opto_param[4]
            

            (optimised_dates, opt) = optimise_dates(dl, k_list, sd, ed, start_year, alpha, beta, gamma, delta, omega)
            
            final_date_list = optimised_dates     

            r = final_date_list

            l = pd.DataFrame(final_locations_list)


            dup = r[r.duplicated()]  # Find duplicates
            dup_Ind = list(dup.index)  # index of duplicates

            r2 = r.drop(r.index[dup_Ind]) # Drop duplicates
            r2 = r2.reset_index(drop = True)  # Reset index
            
            l2 = l.drop(l.index[dup_Ind])  # Drop duplicates
            l2 = l2.reset_index(drop = True)  # Reset index

            l_dates = r2.shape[0]
   

        else:

            r2 = pd.DataFrame(final_date_list)
            l2 = pd.DataFrame(final_locations_list)

            opt = 0

            change_list = 0
            dup_list = 0


    return(r2, l2, opt)
