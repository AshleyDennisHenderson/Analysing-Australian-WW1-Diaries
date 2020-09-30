""" Cleaning WW1 Diaries Data Set - Step 7

This code removes transcribers notes.

Ashley Dennis-Henderson

November 2019"""

## Import Packages ----

import re
import os
import string
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize


## Remove Transcribers Notes ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1f - V1'  # Path to load files

path2 = 'Cleaned Data 1g - V1'  # Path to save files

directory = os.listdir(path)  # Get all filenames

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

        if filename[-3:] == 'txt':  # If text file
    
            n = filename[9:-4]; n = int(n)  # Get document number as int

            text = f.read()  # Read the data

            text = re.sub(r"(\[)([^\[])*?(\])", "", text) # Remove transcriber's notes (1st pass)

            text = re.sub(r"(\[)([^\[])*?(\])", "", text) # Remove transcriber's notes (2nd pass)

            # Note: A 2nd pass is required to remove notes in the form [[]]

            f2 = open(path2 + '/' + filename, 'w+', encoding = 'utf-8')  # Open new file
        
            f2.write(text)  # Write text to new file
        
            f2.close()  # Close file

            text_tokens = word_tokenize(text)  # Tokenize text

            num_tokens = len(text_tokens)  # Count number of words

            df = pd.read_csv(path2 + "/metadata.csv")  # Open metadata.csv
            
            df.set_value(n-1, "Number of Words", num_tokens)  # Update number of words
            
            df.to_csv(path2 + "/metadata.csv", index = False)  # Rewrite metadata.csv

