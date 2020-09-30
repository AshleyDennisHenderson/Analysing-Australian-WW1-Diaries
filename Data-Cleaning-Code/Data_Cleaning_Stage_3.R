
# This file reads in our WW1 diary date/entry csv's and performs the cleaning steps necessary for analysis (Stage 3 of data cleaning)

# Ashley Dennis-Henderson
# September 2020


##  Load Packages ----

pacman::p_load(tidyverse, tidytext, pluralize)


##  Set Working Directory ----

setwd("D:/WW1_Diaries")  # Set Working Directory


##  Create Stop Word List ----

data(stop_words)  # Load stop words data

custom_stop_words <- tribble(
  
  ~word, ~lexicon,
  
  "monday", "DOW",
  "tuesday", "DOW",
  "wednesday", "DOW",
  "thursday", "DOW",
  "friday", "DOW",
  "saturday", "DOW",
  "sunday", "DOW",
  "mon", "DOW",
  "tues", "DOW",
  "tue", "DOW",
  "wed", "DOW",
  "thu", "DOW",
  "thurs", "DOW",
  "fri", "DOW",
  "sat", "DOW",
  "sun", "DOW",
  "lundi", "DOW",
  "lun", "DOW",
  "mar", "DOW",
  "mardi", "DOW",
  "mercredi", "DOW",
  "mer", "DOW",
  "jeudi", "DOW",
  "jeu", "DOW",
  "vendredi", "DOW",
  "ven", "DOW",
  "samedi", "DOW",
  "sam", "DOW",
  "dimanche", "DOW",
  "dim", "DOW",
  "january", "Month",
  "february", "Month",
  "march", "Month",
  "april", "Month",
  "may", "Month",
  "june", "Month",
  "july", "Month",
  "august", "Month",
  "september", "Month",
  "october", "Month",
  "november", "Month",
  "december", "Month",
  "jan", "Month",
  "feb", "Month",
  "feby", "Month",
  "apr", "Month",
  "apl", "Month",
  "aug", "Month",
  "sep", "Month",
  "sept", "Month",
  "septr", "Month",
  "oct", "Month",
  "nov", "Month",
  "dec", "Month",
  "decbr", "Month",
  "janvier", "Month",
  "janv", "Month", 
  "fevrier", "Month",
  "fevr", "Month",
  "février", "Month",
  "févr", "Month",
  "fév", "Month",
  "mars", "Month", 
  "mar", "Month",
  "avril", "Month",
  "avr", "Month",
  "mai", "Month",
  "juin", "Month",
  "juillet", "Month",
  "juil", "Month", 
  "juill", "Month",
  "aout", "Month",
  "août", "Month",
  "septembre", "Month", 
  "octobre", "Month",
  "novembre", "Month",
  "decembre", "Month",
  "décembre", "Month",
  "déc", "Month",
  "st", "Suffix",
  "th", "Suffix",
  "rd", "Suffix",
  "nd", "Suffix",
  "html", "Other",
  "amp", "Other"
  
)  # Create custom stop word list

stop_words2 <- stop_words %>% bind_rows(custom_stop_words)  # Join stop word lists together


##  Create Abbreviations List ----

# This creates a list of common abbreviations and what they equate to

abbrevs<- c('\\babt\\b' = 'about',
            '\\baftn\\b' = 'afternoon',
            '\\barr\\b' = 'arrive',
            '\\barty\\b' = 'artillery',
            '\\baus\\b' = 'australia',
            '\\baust\\b' = 'australia',
            '\\bbn\\b' = 'battalion',
            '\\bbatt\\b' = 'battalion',
            '\\bbattn\\b' = 'battalion',
            '\\bbty\\b' = 'battery',
            '\\bbde\\b' = 'brigade',
            '\\bbtsh\\b' = 'british',
            '\\bcapt\\b' = 'captain', 
            '\\bxma\\b' = 'christmas',
            '\\bcol\\b' = 'colonel', 
            '\\bcoy\\b' = 'company',
            '\\bcpl\\b' = 'corporal',
            '\\bdept\\b' = 'department',
            '\\bdiv\\b' = 'division',
            '\\bdoz\\b' = 'dozen',
            '\\bengr\\b' = 'engineer',
            '\\bgen\\b' = 'general',
            '\\bhq\\b' = 'headquater',
            '\\bhqr\\b' = 'headquater',
            '\\bhdqr\\b' = 'headquater',
            '\\bhosp\\b' = 'hospital',
            '\\binf\\b' = 'infantry',
            '\\binfy\\b' = 'infantry',
            '\\blre\\b' = 'letter',
            '\\blieut\\b' = 'lieutenant', 
            '\\blt\\b' = 'lieutenant',
            '\\bmaj\\b' = 'major',
            '\\bmelb\\b' = 'melbourne',
            '\\bmelbne\\b' = 'melbourne',
            '\\bmorn\\b' = 'morning',
            '\\bpkt\\b' = 'packet',
            '\\bpnr\\b' = 'pioneer',
            '\\bpte\\b' = 'private',
            '\\bpvt\\b' = 'private',
            '\\brwy\\b' = 'railway',
            '\\brec\\b' = 'received',
            '\\brecd\\b' = 'received',
            '\\bregt\\b' = 'regiment',
            '\\breinf\\b' = 'reinforcement',
            '\\bsgt\\b' = 'sergeant',
            '\\bsergt\\b' = 'sergeant',
            '\\bsig\\b' = 'signal',
            '\\bsqn\\b' = 'squadron',
            '\\bsurg\\b' = 'surgeon',
            '\\bsurgn\\b' = 'surgeon',
            '\\byesty\\b' = 'yesterday'
)


##  Load Data ----

ww1_months <- read_csv(file = 'Extracted Dates - [25,1,1,1,1] (ed)/Complete Data Set/entries_months.csv')  # Load months data
ww1_years <- read_csv(file = 'Extracted Dates - [25,1,1,1,1] (ed)/Complete Data Set/entries_years.csv')  # Load years data

##  Remove Punctuation and Numbers ----

months_clean <- ww1_months %>%
  mutate_if(is.character, str_replace_all, pattern = '[[:punct:] ]+', replacement = ' ') %>%  # Remove punctuation
  mutate_if(is.character, str_replace_all, pattern = '[[:digit:] ]+', replacement = ' ') # Remove numbers

months_clean[is.na(months_clean)] <- ''  # Replace months with no entries with an empty string


years_clean <- ww1_years %>%
  mutate_if(is.character, str_replace_all, pattern = '[[:punct:] ]+', replacement = ' ') %>%  # Remove punctuation
  mutate_if(is.character, str_replace_all, pattern = '[[:digit:] ]+', replacement = ' ')  # Remove numbers

years_clean[is.na(years_clean)] <- ''  # Replace years with no entries with an empty string


##  Clean Data and Determine Word Frequencies ----

tidy_months <- months_clean %>%
  unnest_tokens(word, Text) %>%  # Convert dataframe to one row per word
  anti_join(stop_words2) %>%  # Remove stopwords
  mutate(word = singularize(word)) %>%  # Singularise words
  mutate_if(is.character, str_replace_all, abbrevs) %>%  # Replace abbreviations
  count(Month, word, sort = TRUE)  # Count frequency of each word per document

tidy_years <- years_clean %>%
  unnest_tokens(word, Text) %>%  # Convert dataframe to one row per word 
  anti_join(stop_words2) %>%  # Remove stopwords
  mutate(word = singularize(word)) %>%  # Singularise words
  mutate_if(is.character, str_replace_all, abbrevs) %>%  # Replace abbreviations
  count(Year, word, sort = TRUE)  # Count frequency of each word per document

tidy_months_text <- months_clean %>%
  mutate(Text = tolower(Text)) %>%
  mutate_if(is.character, str_replace_all, pattern = '[[:punct:] ]+', replacement = ' ') %>% 
  mutate(Text = singularize(Text)) %>%  # Singularises words
  mutate_if(is.character, str_replace_all, abbrevs) 


