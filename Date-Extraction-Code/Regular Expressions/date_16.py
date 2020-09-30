## IMPORT PACKAGES

import string
import re
from regular_expressions import reg_exp
import errors

def date_form_16(text, date_form = "raw", languages = ['en'], year_prefix = "20"):

    """
    This function takes a string and extracts dates of the form:

                        dd(th|st|rd|nd)


    Parameters
    ----------
    text : str
        The string we wish to parse for dates
    date_form : str (raw or list)
        Whether we want the dates to be given in the raw form from the string,
        or as a list ([dd, mm, yyyy]). The two input options are "raw" and
        "list", with the default being "raw".
    languages : list of str
        What languages we wish to consider. Possible languages are English = 'en',
        French = 'fr' and German = 'de'. The default is just English (['en']).
    year_prefix : str
        A string of length 2 which gives the ? for the date, i.e. for dates known
        to be between 2010 and 2020 the prefix would be '20'. The default is '20'.


    Output
    ------
    date_list : list
        A list of dates with qualities based on the given parameters.
    locations_list : list
        A list containing the locations of the dates within the text.
    text : str
        The original string altered such that it is in lowercase and 
        the text where dates have been found is changed into astericks.


    Author
    ------
    Ashley Dennis-Henderson
    ashley.dennis-henderson@adelaide.edu.au"""



    ## TEST INPUTS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    errors.text_error(text)  # Check text is a string

    errors.date_form_error(date_form)  # Check date_form is "raw" or "list"

   # errors.location_error(location)  # Check location is True or False

    errors.year_prefix_error(year_prefix)  # Check that year_prefix is a string of length 2


    ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    text = text.lower()  # Put text in lowercase
    
    date_list = []  # Create empty list to store dates

    locations_list = []  # Create empty list to store locations


    ## Create Regular Expressions ----

    (date_re, date_re2, month_num_re, date_minimal_re, month_re, year_re, dow_re, joins_re, breaks_re) = reg_exp(languages)  # Obtain regular expressions for required languages
    
    complete_date_RE = re.compile(date_re2)
    
    date_RE = re.compile(date_minimal_re)


    ## Create Date List ----

    for i in complete_date_RE.finditer(text):  # For every string matching our RE
        
        raw_date = i.group()  # Extract raw date

        if date_form == "list":  # If dates should be listed

            for j in date_RE.finditer(raw_date):  # For every string matching our date RE
                
                date = j.group()  # Extract date
                date = int(date)  # Convert date to integer

            month = 0  # Set month to be 0
            year = 0  # Set year to be 0
                
            date_list.append([date, month, year])  # Add date to list

        else:  # If dates should be raw

            date_list.append(raw_date)  # Add date to list

        
        locations_list.append([i.start(), i.end()])  # Add date location to list
        
        n = i.end() - i.start()  # How many characters long the date is
        text = text[:(i.start())] + '*'*(n) + text[(i.end()):]  # Change text where date is to astericks



    return(date_list, locations_list, text)
