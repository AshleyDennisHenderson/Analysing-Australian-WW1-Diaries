""" Cleaning WW1 Diaries Data Set - Step 3 (i)

This code reads in all files from the Cleaned Data 1c folder and counts
the number of square and angled brackets in each file. If a file has a
different number of opening brackets to closing brackets then the code
will terminate, raising an error which gives the name of the file with
uneven brackets as well as the number of opening and closing brackets
in that file.

Ashley Dennis-Henderson

November 2019"""


## Import Packages ----

import os
import string


## Determine Number of Square and Angled Brackets ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1c'  # Path to load files

directory = os.listdir(path)  # Get all filenames

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open the file

        text = f.read()  # Read the data

        n = len(text)  # Number of characters in the text

        num_ls_brac = text.count('[')  # Number of left square brackets
        num_rs_brac = text.count(']')  # Number of right square brackets

        num_la_brac = text.count('<')  # Number of left angled brackets
        num_ra_brac = text.count('>')  # Number of right angled brackets

        #print(filename + '\n') #
        print('[' + str(num_ls_brac) + ', ' + str(num_rs_brac) + ', ' + str(num_la_brac) + ', ' + str(num_ra_brac) + '] \n') #
        #j = 0 #

        if (num_ls_brac != num_rs_brac) or (num_la_brac != num_ra_brac):  # Check if there is an uneven number of brackets
        
##            for i in range(n):  # For every character #
##
##            #if j == 0: #
##
##                text2 = text[0:i]
##
##                if (text2.count('[') - text2.count(']') > 1) or (text2.count('[') - text2.count(']') < 0):
##
##                    #print('[' + str(i) + ', ' + text[i-15:i+15] + '] \n') #
##
##                    #j = 1 #
##                    
##                    print("Square Bracket Error at Character: " + str(i) + ". Surrounding text: " + text[i-10:i+10])
##
##                    raise ValueError('There is an uneven number of brackets in this text: ' + filename + " . There are " + str(num_ls_brac) + " left square brackets, " + str(num_rs_brac) + " right square brackets, " + str(num_la_brac) + " left angled brackets and " + str(num_ra_brac) + " right angled brackets.")
##
##                if (text2.count('<') - text2.count('>') > 1) or (text2.count('<') - text2.count('>') < 0):
##
##                    #print('[' + str(i) + ', ' + text[i-15:i+15] + '] \n') #
##
##                    #j = 1 #
##                    
##                    print("Angled Bracket Error at Character: " + str(i) + ". Surrounding text: " + text[i-10:i+10])
##
##                    raise ValueError('There is an uneven number of brackets in this text: ' + filename + " . There are " + str(num_ls_brac) + " left square brackets, " + str(num_rs_brac) + " right square brackets, " + str(num_la_brac) + " left angled brackets and " + str(num_ra_brac) + " right angled brackets.")

            raise ValueError('There is an uneven number of brackets in this text: ' + filename + " . There are " + str(num_ls_brac) + " left square brackets, " + str(num_rs_brac) + " right square brackets, " + str(num_la_brac) + " left angled brackets and " + str(num_ra_brac) + " right angled brackets.")




        

            

            
