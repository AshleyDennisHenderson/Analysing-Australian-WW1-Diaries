"""  Cleaning WW1 Diaries Data Set - Step 3 (ii)

This code reads in all files from the Cleaned Data 1c folder and if there is
a mismatch in the number of square brackets, prints the text surrounding the
first instance of this.

Ashley Dennis-Henderson

November 2019"""

import os
import string
import numpy as np

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1c'  # Path to load files

directory = os.listdir(path)  # Get all filenames

x = []  # Initiate empty vector
y = []  # Initiate empty vector

count = 0

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open the file

        text = f.read()  # Read the data

        for i in range(len(text)):  # For every character in the text

            if text[i] == '[':  # If the character is a left square bracket

                x.append(i)  # Add the position to vector x
                y.append(1)  # Add 1 to vector y to indicate a left bracket

            if text[i] == ']':  # If the character is a right square bracket

                x.append(i)  # Add the position to vector x
                y.append(-1)  # Add -1 to vector y to indicate a right bracket


    s = np.cumsum(y)  # Determine the cumulative sum of vector y

    for j in range(len(x)):  # For every character position in vector x

        if count == 0:

            if (s[j] > 1) or (s[j] < 0):  # If there is a mismatch in brackets

                print('{' + str(s[j]) + ', ' + str(x[j]) + ', ' + text[(x[j]-15):(x[j]+15)] + '} ')  # Print the text surrounding the mismatched brackets

                count = count + 1


    print('\n')

    # Re-initialise values:
    count = 0
    x = []
    y = []
    
        
        
