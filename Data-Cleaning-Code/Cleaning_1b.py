""" Cleaning WW1 Diaries Data Set - Step 2

This code reads in all files from the Cleaned Data 1a folder and uses regular
expressions to pull metadata from the filenames into a new csv file
(metadata.csv). It also renames every file in the form Document_*.txt,
where * is an integer. Note that this number does not mean anything and the
numbers are based on the order the files are read in. The renamed files and
metadata are saved in the folder: Cleaned Data 1b.

Ashley Dennis-Henderson

October 2019"""


## Import Packages ----

import re
import os
import string
import pandas as pd


## Load List of Possible Author Names ----

colnames = ['ID', 'Last_Name', 'First_Name', 'Other_Names']  # Column names in csv file
data = pd.read_csv('diarists.csv', skiprows = 1, names = colnames)  # Read in diarists csv file

first_names = data.First_Name.tolist()  # Create list of first names
last_names = data.Last_Name.tolist()  # Create list of last names

first_names = map(str.lower, first_names)  # Convert first names to lowercase
last_names = map(str.lower, last_names)  # Convert last names to lowercase

first_names = list(set(first_names))  # Create list of unique first names
last_names = list(set(last_names))  # Create list of unique last names

first_names = ['-' + i + '-' for i in first_names]  # Add hyphens to beginning and end of each first name
last_names = ['-' + i + '-' for i in last_names]  # Add hyphens to beginning and end of each last name

# Note that hypens are added to the beginning and end of each name as the file names have hyphens
# around each word and this reduces the number of false positives (as the list of diarists includes
# just single letters for some first names, i.e. if s was the initial letter it would be picked up
# in the word diaries but -s- wouldn't).


## Create Regular Expressions ----

year_RE = re.compile('19\d{2}')
month_RE = re.compile('(january|february|march|april|may|june|july|august|september|october|november|december)')
type_RE = re.compile('(letter-diary|narrative|diary|letter)')
item_RE = re.compile('item-\d{2}')
node_RE = re.compile('\d{5,6}')
firstname_RE = re.compile("|".join(first_names))
lastname_RE = re.compile("|".join(last_names))
page_RE = re.compile('\[((p|P)age \d+)\]')


## Rename Files and Create Metadata ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Condensed Data'  # Path to load files

path2 = 'Renamed Data'  # Path to save files

filenames = os.listdir(path)  # Get all filenames

document_num = 1  # Counter for document number

column_names = ['Document Name', 'Original Title', 'Document Type', 'Author First Name',
                'Author Last Name', 'Item Number', 'Start Month', 'Start Year', 'End Month',
                'End Year', 'Receiver', 'Regarding', 'Number of Pages', 'Number of Words', 'Node']  # Metadata Column Names

metadata = pd.DataFrame(columns = column_names)  # Create empty dataframe

metadata.to_csv(path2 + '/metadata.csv', index = False)  # Save dataframe as csv

# Notes:
#       - Columns Item Number, Start Month, Start Year, End Month, End Year,
#         Number of Pages, Number of Words and Node are all integer columns.
#         Hence, when these values are unknown we enter 0 (which is not a
#         possible true value for any of these columns).
#       - All other columns are character columns and hence when these are
#         not known we give it an empty string.
#       - Number of Words cannot yet be calculated and hence will be set to
#         0 for all documents


for filename in filenames:  # For every filename

    document_name = 'Document_' + str(document_num)  # Create document name

    original_title = filename  # Get original title


    # Create file with new name

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file
    
        text = f.read()  # Read the data
    
        f2 = open(path2 + '/' + document_name + '.txt', 'w+', encoding = 'utf-8')  # Open new file
    
        f2.write(text)  # Write text to new file
    
        f2.close()  # Close file


    # Find Document Type

    j = 1; document_type = 'other'  # Initially set type to other

    for i in type_RE.finditer(filename):  # For any match to the type RE

        if j == 1:  # If it is the first match

            raw_type = i.group()  # Get raw match

            document_type = raw_type.replace('-', ' ')  # Update document type

        j = j + 1
        

    # Find Author First Name

    j = 1; author_first = ''  # Initially set first name to empty string

    for i in firstname_RE.finditer(filename):  # For any match to the firstname RE

        if j == 1:  # If it is the first match

            raw_name = i.group()  # Get raw match

            author_first = raw_name[1:-1]  # Update author first name

        j = j + 1
        

    # Find Author Last Name

    j = 1; author_last = ''  # Initially set last name to empty string

    for i in lastname_RE.finditer(filename):  # For any match to the lastname RE

        if j == 1:  # If it is the first match

            raw_name = i.group()  # Get raw match

            author_last = raw_name[1:-1]  # Update author last name

        j = j + 1
        

    # Find Item Number

    j = 1; item_num = 1  # Initially set item number to 1

    for i in item_RE.finditer(filename):  # For any match to the item RE

        if j == 1:  # If it is the first match

            raw_item = i.group()  # Get raw match

            item_num = int(raw_item[-2:])  # Update item number (as int)

            j = j + 1


    # Find Start and End Month

    j = 1; start_month = 0; end_month = 0  # Initially set start and end month to 0

    for i in month_RE.finditer(filename):  # For any match to the month RE

        if j == 1:  # If it is the first match

            raw_month = i.group()  # Get raw month

            # Update start month:

            if raw_month == 'january':

                start_month = 1

            elif raw_month == 'february':

                start_month = 2

            elif raw_month == 'march':

                start_month = 3

            elif raw_month == 'april':

                start_month = 4

            elif raw_month == 'may':

                start_month = 5

            elif raw_month == 'june':

                start_month = 6

            elif raw_month == 'july':

                start_month = 7

            elif raw_month == 'august':

                start_month = 8

            elif raw_month == 'september':

                start_month = 9

            elif raw_month == 'october':

                start_month = 10

            elif raw_month == 'november':

                start_month = 11

            elif raw_month == 'december':

                start_month = 12

        if j == 2:  # If it is the second match

            raw_month = i.group()  # Get raw month

            # Update end month:

            if raw_month == 'january':

                end_month = 1

            elif raw_month == 'february':

                end_month = 2

            elif raw_month == 'march':

                end_month = 3

            elif raw_month == 'april':

                end_month = 4

            elif raw_month == 'may':

                end_month = 5

            elif raw_month == 'june':

                end_month = 6

            elif raw_month == 'july':

                end_month = 7

            elif raw_month == 'august':

                end_month = 8

            elif raw_month == 'september':

                end_month = 9

            elif raw_month == 'october':

                end_month = 10

            elif raw_month == 'november':

                end_month = 11

            elif raw_month == 'december':

                end_month = 12
                
        j = j + 1

    
                
    # Find Start and End Year

    j = 1; start_year = 0; end_year = 0  # Initially set start and end year to 0

    for i in year_RE.finditer(filename):  # For any match to the year RE

        if j == 1:  # If it is the first match

            raw_year = i.group()  # Get raw match

            start_year = int(raw_year)  # Update start year (as int)

        if j == 2:  # If it is the second match

            raw_year = i.group()  # Get raw match

            end_year = int(raw_year)  # Update end year (as int)

        j = j + 1


    # Number of pages

    num_pages = 0  # Initially set number of pages to zero

    for i in page_RE.finditer(text):  # For every match to the page RE

        num_pages = num_pages + 1  # Increase the number of pages by 1
        

    # Node Number

    for i in node_RE.finditer(filename):  # For every match to the node RE

        raw_node = i.group()  # Get raw match

        node = int(raw_node)  # Update node number (as int)

    # Note:
    #       - There may be a case where there is two numbers of length 5 or 6
    #         in the filename, however, the node number is always last. The
    #         above for loop will write over any previous number and only
    #         keep the last match
        

    print('\n' + filename + '\n')  # Print original filename
    

    # Check Document Type

    print('Type: ' + document_type)  # Print document type

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        document_type = input('What is it? ')  # Have user input correct file type
        

    # Check Author First Name

    print('\n' + 'Author First Name: ' + author_first)  # Print author first name

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        author_first = input('What is it? ')  # Have user input correct author first name
        

    # Check Author Last Name

    print('\n' + 'Author Last Name: ' + author_last)  # Print author last name

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        author_last = input('What is it? ')  # Have user input correct author last name
        

    # Check Item Number

    print('\n' + 'Item Number: ' + str(item_num))  # Print item number

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        item_num = input('What is it? ')  # Have user input correct item number
        item_num = int(item_num)  # Convert item number to int
        

    # Check Start Month

    print('\n' + 'Start Month: ' + str(start_month))  # Print start month

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        start_month = input('What is it? ')  # Have user input correct start month
        start_month = int(start_month)  # Convert start month to int
        

    # Check Start Year

    print('\n' + 'Start Year: ' + str(start_year))  # Print start year

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        start_year = input('What is it? ')  # Have user input correct start year
        start_year = int(start_year)  # Convert start year to int
        

    # Check End Month

    print('\n' + 'End Month: ' + str(end_month))  # Print end month

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        end_month = input('What is it? ')  # Have user input correct end month
        end_month = int(end_month)  # Convert end month to int
        

    # Check End Year

    print('\n' + 'End Year: ' + str(end_year))  # Print end year

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        end_year = input('What is it? ')  # Have user input correct end year
        end_year = int(end_year)  # Convert end year to int
        

    # Check Receiver

    receiver = ''  # Set receiver to empty string

    print('\n' + 'Receiver: ')  # Print receiver (currently empty)

    correct = input('Is this required: ')  # Ask user if receiver is required

    if correct == 'n':  # If required

        receiver = input('What is it? ')  # Have user input receiver
        

    # Check Regarding
    
    regarding = ''  # Set regarding to empty string

    print('\n' + 'Regarding: ')  # Print regarding (currently empty)

    correct = input('Is this required: ')  # Ask user if regarding is required

    if correct == 'n':  # If required

        regarding = input('What is it? ')  # Have user input regarding

    # Notes:
    #       - Regarding may be a person, place, battle, or event. It is what the
    #       - document was written about
    

    # Check Node Number

    print('\n' + 'Node: ' + str(node))  # Print node number

    correct = input('Is this correct: ')  # Ask user if it is correct

    if correct == 'n':  # If incorrect

        node = input('What is it? ')  # Have user input node number
        node = int(node)  # Convert node number to int
        
        
    # Add to Metadata

    values = [[document_name, original_title, document_type, author_first, author_last, item_num,
               start_month, start_year, end_month, end_year, receiver, regarding, num_pages, 0, node]]  # Create list of metadat values

    temp = pd.DataFrame(values, columns = column_names)  # Create pandas dataframe
    
    temp.to_csv(path2 + '/metadata.csv', mode = 'a', header = False, index = False)  # Add dataframe to csv file
    
    
    # Increase document number

    document_num = document_num + 1  # Increase document number by 1


