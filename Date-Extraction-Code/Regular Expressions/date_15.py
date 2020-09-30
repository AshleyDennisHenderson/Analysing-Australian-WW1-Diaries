## This file contains the function date_form_15

## Import Packages ----

import re
import string
from regular_expressions import reg_exp
from Convert_Months import convert_month


## Function ----

def date_form_15(text, date_form = 'raw', languages = ['en'], year_prefix = '20'):

    """

        DOW D


    """

    
    text = text.lower()  # Convert text to lowercase

    date_list = []  # Create empty list to store dates

    locations_list = []  # Create empty list to store locations of dates
    

    (date_re, date_re2, month_num_re, date_minimal_re, month_re, year_re, dow_re, joins_re, breaks_re) = reg_exp(languages)  # Obtain regular expression building blocks for required languages


    complete_RE = re.compile(dow_re + breaks_re + date_re)  # RE to extract entire date

    date_RE = re.compile(date_minimal_re)  # RE to match just the date


    for i1 in complete_RE.finditer(text):  # For every piece of text matching our RE

        raw_date = i1.group()  # Get raw date


        if date_form == "list":  # If dates should be in list form
            

            counter = 0

            for i2 in date_RE.finditer(raw_date):  # For every piece of text matching our date RE

                counter = counter + 1  # Add to counter

                if counter == 1:  # If it is the first string matching our date RE

                    date = i2.group()  # Get date
                    date = int(date)  # Convert date to integer


            month = 0
            year = 0


            date_list.append([date, month, year])  # Add date to list


        else:  # If dates should be in raw form

            date_list.append(raw_date)  # Add date to list


        locations_list.append([i1.start(), i1.end()])  # Add date location to list


        n = i1.end() - i1.start()  # Get length of date

        text = text[:(i1.start())] + '*'*(n) + text[(i1.end()):]  # Change text where date is to astericks ^

        # ^ This is so that dates are not extracted multiple times


    return(date_list, locations_list, text)
