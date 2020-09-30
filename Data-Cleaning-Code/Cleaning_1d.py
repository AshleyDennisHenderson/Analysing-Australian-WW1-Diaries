""" Cleaning WW1 Diaries Data Set - Step 4

This code reads in all files from the Cleaned Data 1c folder then
converts the html text to regular text. It also determines the 
number pages in each document and adds this to metadata.csv.
The cleaned files are saved in the folder: Cleaned Data 1d.

Note, this code requires the files Edited_Brackets and metadata.csv to have first been copied into folder
Cleaned Data 1d

Ashley Dennis-Henderson

November 2019"""


## Import Packages ----

import re
import os
import string
import pandas as pd
from bs4 import BeautifulSoup


## Clean Files and Update Metadata ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1c'  # Path to load files

path2 = 'Cleaned Data 1d'  # Path to save files

directory = os.listdir(path)  # Get all filenames

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

        if filename[-3:] == 'txt':  # If text file
    
            n = filename[9:-4]; n = int(n)  # Get document number as int

            text = f.read()  # Read the data

            soup = BeautifulSoup(text)

            text = soup.get_text(separator = '\n')  # Convert from html text to regular text

            text = re.sub(r"\n", " ", text)  # Convert \n to single space

            f2 = open(path2 + '/' + filename, 'w+', encoding = 'utf-8')  # Open new file
        
            f2.write(text)  # Write text to new file
        
            f2.close()  # Close file

            # Determine Number of Pages:

            page_RE = re.compile('\[( )?((p|P)age)( )?(\d+)( )?\]')

            num_pages = 0  # Initially set number of pages to zero

            for i in page_RE.finditer(text):  # For every match to the page RE

                num_pages = num_pages + 1  # Increase the number of pages by 1


            df = pd.read_csv(path2 + "/metadata.csv")  # Open metadata.csv
            
            df.set_value(n-1, "Number of Pages", num_pages)  # Update number of words
            
            df.to_csv(path2 + "/metadata.csv", index = False)  # Rewrite metadata.csv
