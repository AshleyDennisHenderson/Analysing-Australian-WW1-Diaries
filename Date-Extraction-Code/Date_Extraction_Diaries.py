
# Ashley Dennis-Henderson
# June 2020

## Import Packages ----

import pandas as pd
import os
import sys
import spacy
from spacy import displacy
import re
sys.path.append('D:\date-extraction')

from date_extraction import extract_dates
from date_conversions import convert_to_epoch

## Set working directory and read in metadata ----

wd = 'D:\\WW1_Diaries'  # Working directory path

os.chdir(wd)  # Change working directory

path = 'Cleaned Data 1i - V1'  # Path for raw data

directory = os.listdir(path)  # Get all filenames from our path

directory = sorted(directory)  # Sort directory

metadata = pd.read_csv(path + '/metadata.csv')  # Load metadata


## Initialise ----

opt_params = [1]
opt_params2 = [125, 150, 175, 200]

num_params = len(opt_params)
n2 = len(opt_params2)

for p in range(n2):

    alpha = opt_params2[p]

    for p2 in range(num_params):

        delta = opt_params[p2]

        folder = 'Extracted Dates - [' + str(alpha) + ',1,1,' + str(delta) + ',1] (ed)'

        os.makedirs(folder)

        os.makedirs(folder + '/Complete Data Set')
        os.makedirs(folder + '/Dates')
        os.makedirs(folder + '/Entries Epoch')
        os.makedirs(folder + '/Entries Exp')
        os.makedirs(folder + '/Locations')
        os.makedirs(folder + '/No Dates')
        os.makedirs(folder + '/Opt')

        entries_exp = []
        entries_epoch = []
        count = 0
        opt2 = []

        diaries = []

        res_change = []
        res_dup = []
        

        for filename in directory:  # For every filename in the directory

            with open(path + '/' + filename, 'r', encoding = 'utf-8') as f:  # Open each file

                if filename[-3:] == 'txt':  # If text file

                    fn = filename

                    ID = int(filename[9:-4])  # Document number
                    print(ID)

                    if os.path.exists(folder + '/Entries Exp/Entries_Exp_Document_' + str(ID) + '.csv'):  # If this has been run

                        # Read in results

                        results_exp = pd.read_csv(folder + '/Entries Exp/Entries_Exp_Document_' + str(ID) + '.csv', index_col = False)

                        diary_entries_exp = results_exp.values.tolist()

                        results_epoch = pd.read_csv(folder + '/Entries Epoch/Entries_Epoch_Document_' + str(ID) + '.csv', index_col = False)

                        diary_entries_epoch = results_epoch.values.tolist()

                    else:

                        diary_entries_exp = []  # Initialise empty list

                        diary_entries_epoch = []  # Initialise empty list

                        text = f.read()  # Read the data

                        sm = metadata.iloc[ID-1, 6]  # Get start month
                        sy = metadata.iloc[ID-1, 7]  # Get start year

                        if sm == 0:

                            sm = 1

                        if sy == 0:

                            sy = 1914

                        em = metadata.iloc[ID-1, 8]  # Get END month
                        ey = metadata.iloc[ID-1, 9]  # Get END year
                        
                        if em == 0:

                            em = 12

                        if ey == 0:

                            ey = 1920

                        # Get start date # Update code

                        (e_dates, locations, opt, change, dup) = extract_dates(text, date_form = "list", languages = ['en', 'fr'], optimise = True, date_type = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], start_date = [1,sm,sy], end_date = [31,em,ey], year_prefix = '19', start_year = 1914, opto_param = [alpha,1,1,delta,1])  # Extract date

                        res_change.append([ID] + change)
                        res_dup.append([ID] + dup)
                        
                        e_list = e_dates.values.tolist()

                        e_list = convert_to_epoch(e_list, 1914)

                        l = len(e_list)

                        if opt == -10:  # No dates found

                            opt2 = pd.DataFrame([0], columns = ['opt'])
                            opt2.to_csv(folder + '/No Dates/No_Dates_Document_' + str(ID) + '.csv', index = False)

                        else:  # Dates found

                            if opt == 0:

                                opt2 = pd.DataFrame([0], columns = ['opt'])
                                opt2.to_csv(folder + '/Opt/Optimisation_Incomplete_Document_' + str(ID) + '.csv', index = False)
                 
                            if int(locations.iloc[0,0]) != 0:  # If the first extracted date is not the first thing in the text
                                    
                                entry = text[:(int(locations.iloc[0,0]))]  # Create entry
                                
                                entry = re.sub(r'(\xa0)+', '', entry)
                                entry = re.sub(r'( )+', ' ', entry)
                                    
                                diary_entries_exp.append([ID, 'unknown', 'unknown', 'unknown', entry])  # Save entry to list(expanded form)

                                diary_entries_epoch.append([ID, 'unknown', entry])  # Save entry to list (epoch form)
                                    
                            for j in range(l-1):  # For every date except the last one
                                    
                                entry = text[int(locations.iloc[j,1]):int(locations.iloc[j+1,0]-1)] # Create entry

                                entry = re.sub(r'(\xa0)+', '', entry)
                                entry = re.sub(r'( )+', ' ', entry)
                                    
                                diary_entries_exp.append([ID, e_dates.iloc[j,0], e_dates.iloc[j,1], e_dates.iloc[j,2], entry])  # Save entry to list(expanded form)

                                diary_entries_epoch.append([ID, e_list[j], entry])  # Save entry to list (epoch form)

                                    
                            entry = text[int(locations.iloc[l-1,1]):]  # Create final entry

                            entry = re.sub(r'(\xa0)+', '', entry)
                            entry = re.sub(r'( )+', ' ', entry)
                                
                            diary_entries_exp.append([ID, e_dates.iloc[l-1,0], e_dates.iloc[l-1,1], e_dates.iloc[l-1,2], entry])  # Save entry to list (expanded form)

                            diary_entries_epoch.append([ID, e_list[l-1], entry])

                            df = e_dates.rename(columns={0: "D", 1: "M", 2: "Y"})
                            locations2 = locations.rename(columns={0: "Start", 1: "End"})

                            df.to_csv(folder + '/Dates/Extracted_Dates_Document_' + str(ID)+ '.csv', index = False)
                            
                            locations2.to_csv(folder + '/Locations/Date_Locations_Document_' + str(ID)+ '.csv', index = False)

                            diary_entries_exp_pd = pd.DataFrame(diary_entries_exp, columns = ['ID', 'D', 'M', 'Y', 'Entry'])

                            diary_entries_epoch_pd = pd.DataFrame(diary_entries_epoch, columns = ['ID', 'Date', 'Entry'])

                            diary_entries_exp_pd.to_csv(folder + '/Entries Exp/Entries_Exp_Document_' + str(ID) + '.csv', index = False)

                            diary_entries_epoch_pd.to_csv(folder + '/Entries Epoch/Entries_Epoch_Document_' + str(ID) + '.csv', index = False)


                    entries_exp = entries_exp + diary_entries_exp
                    entries_epoch = entries_epoch + diary_entries_epoch




        ## Create Dataframe ---

        entries_exp_pd = pd.DataFrame(entries_exp, columns = ['ID', 'D', 'M', 'Y', 'Entry'])

        entries_epoch_pd = pd.DataFrame(entries_epoch, columns = ['ID', 'Date', 'Entry'])

        res_change_pd = pd.DataFrame(res_change, columns = ['ID', 'Changed', 'Num', 'Prop'])

        res_dup_pd = pd.DataFrame(res_dup, columns = ['ID', 'Duplicated', 'Num', 'Prop'])


        ## Create csv ----

        entries_exp_pd.to_csv(folder + '/Complete Data Set/entries_exp.csv', index = False)

        entries_epoch_pd.to_csv(folder + '/Complete Data Set/entries_epoch.csv', index = False)

        res_change_pd.to_csv(folder + '/Complete Data Set/res_change.csv', index = False)

        res_dup_pd.to_csv(folder + '/Complete Data Set/res_dup.csv', index = False)



