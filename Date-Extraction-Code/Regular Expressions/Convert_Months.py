## This file contains the function convert_month

## Function ----

def convert_month(month_raw):

    """ Converts the word version of a month (in english or french) to the equivalent number"""

    ## January (1) ----

    if month_raw[0:3] == 'jan':
        month = 1

    ## February (2) ----
        
    elif month_raw[0:3] == 'feb':
        month = 2

    elif month_raw[0:3] == 'fev':  # FRENCH
        month = 2
        
    elif month_raw[0:3] == 'fév':  # FRENCH
        month = 2

    ## March (3) ----
        
    elif month_raw[0:3] == 'mar':
        month = 3

    ## April (4) ----
        
    elif month_raw[0:2] == 'ap':
        month = 4
        
    elif month_raw[0:2] == 'av':  # FRENCH
        month = 4

    ## May (5) ----
        
    elif month_raw[0:3] == 'may':
        month = 5
        
    elif month_raw[0:3] == 'mai':  # FRENCH
        month = 5

    ## June (6) ----
        
    elif month_raw[0:3] == 'jun':
        month = 6
        
    elif month_raw[0:4] == 'juin':  # FRENCH
        month = 6

    ## July (7) ----
        
    elif month_raw[0:3] == 'jul':
        month = 7
        
    elif month_raw[0:4] == 'juil':  # FRENCH
        month = 7

    ## August (8) ----
        
    elif month_raw[0:3] == 'aug':
        month = 8
        
    elif month_raw[0:2] == 'ao':  # FRENCH
        month = 8

    ## September (9) ----
        
    elif month_raw[0:3] == 'sep':
        month = 9

    ## October (10) ----
        
    elif month_raw[0:3] == 'oct':
        month = 10

    ## November (11) ----
        
    elif month_raw[0:3] == 'nov':
        month = 11

    ## December (12) ----
        
    elif month_raw[0:3] == 'dec':
        month = 12
        
    elif month_raw[0:3] == 'déc':  # FRENCH
        month = 12


    return(month)
