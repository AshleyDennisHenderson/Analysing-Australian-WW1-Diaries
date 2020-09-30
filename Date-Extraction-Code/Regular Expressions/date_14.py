## This file contains the function date_form_14

## Import Packages ----

import re
import string
from regular_expressions import reg_exp
from Convert_Months import convert_month


## Function ----

def date_form_14(text, date_form = 'raw', languages = ['en'], year_prefix = '20'):

    """

        Y DOW M D


    """
    

    text = text.lower()  # Convert text to lowercase

    date_list = []  # Create empty list to store dates

    locations_list = []  # Create empty list to store locations of dates
    

    (date_re, date_re2, month_num_re, date_minimal_re, month_re, year_re, dow_re, joins_re, breaks_re) = reg_exp(languages)  # Obtain regular expression building blocks for required languages


    complete_RE = re.compile("(" + "(')?" + year_re + breaks_re + ")?" + "(" + dow_re + breaks_re + ")?" + month_re + breaks_re + date_re)  # RE to extract entire date

    date_RE = re.compile(date_minimal_re)  # RE to match just the date

    month_RE = re.compile(month_re)  # RE to match just the month

    year_RE = re.compile(year_re)  # RE to match just the year


    for i1 in complete_RE.finditer(text):  # For every piece of text matching our RE

        raw_date = i1.group()  # Get raw date


        if date_form == "list":  # If dates should be in list form
            

            counter = 0

            for i2 in date_RE.finditer(raw_date):  # For every piece of text matching our date RE

                date = i2.group()  # Get date
                l = len(date)  # Get length of date
                date = int(date)  # Convert date to integer


            for i3 in month_RE.finditer(raw_date):  # For every piece of text matching our month RE

                raw_month = i3.group()  # Get month

                month = convert_month(raw_month)  # Find the integer value equivalent to this month


            year = 0  # Initialise year to 0 in case there was no year in the date

            counter2 = 0

            num = len(re.findall(year_re, raw_date))  # Find number of matches for year re

            if (num == 1) and (l ==2):  # If there is only one match and length of date is 2

                year = 0  # There is no year in the string

            else:  # There is a year

                for i4 in year_RE.finditer(raw_date):  # For every piece of text matching our year RE

                    raw_year = i4.group()  # Get year

                    counter2 = counter2 + 1  # Add to counter

                    if counter2 == 1:  # If first match

                        if len(raw_year) == 2:  # If the year only contains two characters

                            raw_year = year_prefix + raw_year  # Add the year prefix

                        year = int(raw_year)  # Convert year to integer


            date_list.append([date, month, year])  # Add date to list


        else:  # If dates should be in raw form

            date_list.append(raw_date)  # Add date to list


        locations_list.append([i1.start(), i1.end()])  # Add date location to list


        n = i1.end() - i1.start()  # Get length of date

        text = text[:(i1.start())] + '*'*(n) + text[(i1.end()):]  # Change text where date is to astericks ^

        # ^ This is so that dates are not extracted multiple times


    return(date_list, locations_list, text)
