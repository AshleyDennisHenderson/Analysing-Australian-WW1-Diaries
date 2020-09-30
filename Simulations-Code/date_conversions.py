def convert_to_epoch(date_list, start_year = 2000):

    """
    This function takes a list of lists of the form [dd, mm, yyyy] and converts it to
    the number of days since the 1st January in the given start year.
    
	
    Parameters
    ----------
    date_list : list (int)
        This is a list of a list of dates [dd, mm, yyyy] that we wish to convert
        into the number of days since 1st January in the given start year.
    start_year : int
        The year for which we want to know the number of days since. The default 
        value is 2000.


    Output
    ------
    x : list (int)
        A list containing the conversions of the given dates into the number of days
        since 1st January in the given start year.


    Author
    ------
    Ashley Dennis-Henderson
    ashley.dennis-henderson@adelaide.edu.au"""


    x = []  # Create empty list
    
    l = len(date_list)  # Find the number of dates
    
    for i in range(l):  # For every date in the list

        Y = (date_list[i])[2]  # Extract the year
        M = (date_list[i])[1]  # Extract the month
        D = (date_list[i])[0]  # Extract the date
        
        x.append(372*(Y-start_year) + 31*(M-1) + D - 1)  # Convert the date into a number

    return(x)


def convert_to_expanded(x, start_year = 2000):

    """
	This function takes a list of the number of days since the 1st January in
	the given start year and converts to a list of lists of the form [dd, mm, yyyy].

	
	Parameters
	----------
	x : list (int)
	    A list containing the number of days since 1st January in the given start
	    year.
	date_list : list (int)
	    This is a list of a list of dates [dd, mm, yyyy] that we wish to convert
	    into the number of days since 1st January in the given start year.
	start_year : int
	    The year for which we want to know the number of days since. The default 
	    value is 2000.


	Output
	------
	date_list : list (int)
	    This is a list of a list of dates [dd, mm, yyyy] that we have converted
	    from the number of days since 1st January in the given start year.


	Author
	------
	Ashley Dennis-Henderson
	ashley.dennis-henderson@adelaide.edu.au"""
    

    date_list = []  # Create empty list
    
    l = len(x)  # Find the number of dates
    
    for i in range(l):  # For every date

        Y1 = x[i] // 372  # Quotient of x/372
        R1 = x[i] - Y1*372  # Remainder of x/372
        Y = Y1 + start_year  # Year

        M1 = R1 // 31  # Quotient of R1/31
        R2 = R1 - M1*31  # Remainder of R1/31
        M = M1 + 1  # Month

        D = R2 + 1  # Date
        
        date_list.append([D, M, Y])  # Add date to list

    return(date_list)
