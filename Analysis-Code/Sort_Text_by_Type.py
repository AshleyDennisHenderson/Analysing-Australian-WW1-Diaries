import pandas as pd
import os
import sys


wd = 'D:\\WW1_Diaries'  # Working directory path

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1g - V1'  # Path for raw data

directory = os.listdir(path)  # Get all filenames from our path

directory = sorted(directory)  # Sort directory

metadata = pd.read_csv(path + '/metadata.csv')  # Load metadata


diary_text = ''
letter_text = ''
narrative_text = ''
LD_text = ''
other_text = ''

for filename in directory:  # For every filename in the directory

    with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

        if filename[-3:] == 'txt':  # If text file

            fn = filename

            ID = int(filename[9:-4])  # Document number

            text = f.read()  # Read the data

            doc_type = metadata.iloc[ID-1, 2]  # Get document type

            if doc_type == 'diary':

                diary_text = diary_text + ' ' + text

            if doc_type == 'letter':

                letter_text = letter_text + ' ' + text

            if doc_type == 'letter diary':

                LD_text = LD_text + ' ' + text

            if doc_type == 'narrative':

                narrative_text = narrative_text + ' ' + text

            if doc_type == 'other':

                other_text = other_text + ' ' + text

data = pd.DataFrame([[diary_text, 'Diary'], [letter_text, 'Letter'], [LD_text, 'Letter-Diary'], [narrative_text, 'Narrative'], [other_text, 'Other']], columns = ['text', 'Type'])  # Create empty dataframe
data.to_csv('Data_Sorted_by_Type.csv', index = False)
