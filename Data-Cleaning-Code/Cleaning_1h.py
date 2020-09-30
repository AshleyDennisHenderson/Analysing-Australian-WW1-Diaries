""" Cleaning WW1 Diaries Data Set - Step 8

This code filters for only non-empty diaries.

Ashley Dennis-Henderson

November 2019"""

## csvs have to already  be in folder

## Import Packages ----

import re
import os
import string
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize

## Remove Transcribers Notes ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1g - V1'  # Path to load files

path2 = 'Cleaned Data 1h - V1'  # Path to save files

directory = os.listdir(path)  # Get all filenames

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

        if filename[-3:] == 'txt':  # If text file
    
            n = filename[9:-4]; n = int(n)  # Get document number as int

            df = pd.read_csv(path2 + "/metadata.csv")  # Open metadata.csv

            if df.iloc[n-1, 2] == 'diary':  # If diary

                if df.iloc[n-1, 13] > 0:  # If non-empty

                    text = f.read()  # Read the data

                    f2 = open(path2 + '/' + filename, 'w+', encoding = 'utf-8')  # Open new file
        
                    f2.write(text)  # Write text to new file
        
                    f2.close()  # Close file
            
    
