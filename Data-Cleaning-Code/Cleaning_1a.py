""" Cleaning WW1 Diaries Data Set - Step 1

This code reads in all folders from the WW1 Diaries raw data set, extracts the
content from the JSON page files and combines them to form a single text file
per document with the same name as the original folder. These text files are
saved in the folder: Cleaned Data 1a.

Ashley Dennis-Henderson

October 2019"""


## Import Packages ----

import os
import json


## Clean Data ----

wd = 'D:\\WW1_Diaries'  # Working directory path

os.chdir(wd)  # Change working directory

path = 'Raw Data'  # Path for raw data

directory = os.listdir(path)  # Get all filenames from our path


for filename in directory:  # For every filename in the directory
    
    if os.path.isdir(os.path.join(os.path.abspath("."), path + '/' + filename)):  # If it is a subfolder

        subpath = path + '/' + filename  # Path for subfolder
        
        subdirectory = os.listdir(subpath)  # Get all filenames for our subpath
        
        subdirectory = sorted(subdirectory, key=lambda x: int(x.split('-')[1]))  # Sort subdirectory such that pages are in order

        complete_text = ''  # Initialise empty string to save content to

        for filename2 in subdirectory:  # For every file in subfolder

            with open(subpath + '/' + filename2, 'r', encoding = 'utf-8') as f:  # Open each file

                datastore = json.load(f)  # Load file into datastore

                if datastore['body'] == []:  # If the body section is empty

                    text = ''  # There is no content for that page

                else:

                    text = datastore['body']['value']  # Get content

                complete_text = complete_text + text + '\n'  # Add content to complete text


        new_filename = 'Clean_Data_1a\\' + filename + '.txt'  # Filename for text file
        
        f = open(new_filename, "w+", encoding = 'utf-8')  # Create text file
        
        f.write(complete_text)  # Add content to text file
        
        f.close()  # Close text file

