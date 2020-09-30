""" Cleaning WW1 Diaries Data Set - Step 6

This file extracts text within square brackets, removes numbers and punctuation then
determines what percentage of transcribers notes are date related.

Ashley Dennis-Henderson

October 2019"""

## Import Packages ----

import re
import os
import string
from nltk.tokenize import sent_tokenize, word_tokenize


## Regular Expressions ----

month_EN = "(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|feby|mar|apr|apl|aug|septr|sept|sep|oct|nov|dec)"
dow_EN = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|mon|tues|tue|wed|thurs|thu|fri|sat|sun)"

month_FR = "(janvier|fevrier|mars|avril|mai|juin|juillet|aout|septembre|octobre|novembre|decembre|février|décembre|janv|fevr|juil|févr|août|déc)"
dow_FR = "(lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche)"

month_DE = "(januar|februar|marz|mai|juni|juli|oktober|dezember|märz|jän|märz|mai|juni|juli|okt|dez)"
dow_DE = "(montag|dienstag|mittwoch|donnerstag|freitag|samstag|sonntag)"

#date = "(\d{1,2}/\d{1,2}/\d{2,4})"

date_re = re.compile('(' + month_EN + '|' + month_FR + '|' + month_DE + '|' + dow_EN + '|' + dow_FR + '|' + dow_DE + ')( |$)')


## Open Each File ----

wd = 'D:\\WW1_Diaries'  # Working directory

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1e'  # Path to load files

directory = os.listdir(path)  # Get all filenames

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

        if filename[-3:] == 'txt':  # If text file

            text = f.read()  # Read the data

            n = len(text)  # Number of characters

            if n > 0:

                notes = ''

                num_left = 0
                num_right = 0
                left_pos = 0
                right_pos = 0

                for i in range(n):  # For every character

                    char = text[i]

                    if char == '[': # If the character is a left bracket

                        num_left = num_left + 1 # Increase counter for left brackets

                        if num_left == 1:

                            left_pos = i # Add the index to the list

                    elif char == ']': # If the charater is a right bracket

                        num_right = num_right + 1 # Increase counter for right brackets

                        right_pos = i # Add the index to the list

                    if (num_left == num_right) and (num_left != 0): # If we have same number of left and right brackets (not zero)

                        notes = notes + text[left_pos:right_pos+1] + ' '
                        
                        num_left = 0
                        num_right = 0

                        left_pos = 0
                        right_pos = 0

                        
                notes = re.sub(r"]", " ", notes)
                notes = re.sub(r"\[", " ", notes)
                notes = re.sub(r'[^\w\s]', '', notes)  # Remove any punctuation
                notes = re.sub(r'[\d]', '', notes)  # Remove any numbers
                notes = notes.lower()
                
                count = 0
                
                for j in date_re.finditer(notes):  # For every match in our notes

                    count = count + 1

                text_tokens = word_tokenize(text)  # Tokenize text

                num_tokens = len(text_tokens)  # Count number of words

                percentage = count/num_tokens * 100

                if percentage > 0.5 and percentage <= 1:

                    print('\n\n' + filename + '\n\n' + str(percentage) + '\n\n' + notes + '\n\n' + filename + '\n\n')

                    input('Next file?')
                  
                


            

