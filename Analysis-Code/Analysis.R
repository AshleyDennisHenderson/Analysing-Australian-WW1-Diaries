
## This code performs analysis for our WW1 diaries based on the tutorial (https://cran.r-project.org/web/packages/ldatuning/vignettes/topics.html)

## June 2020


##  Load Packages ----

pacman::p_load(tidyverse, tidytext, pluralize, ggwordcloud, zoo, topicmodels, xtable, lexicon, leaflet, ngram, ggplot2, ldatuning)


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

months_clean[is.na(months_clean)] <- ''  # Replace months with no entries with empty string


years_clean <- ww1_years %>%
  mutate_if(is.character, str_replace_all, pattern = '[[:punct:] ]+', replacement = ' ') %>%  # Remove punctuation
  mutate_if(is.character, str_replace_all, pattern = '[[:digit:] ]+', replacement = ' ')  # Remove numbers

years_clean[is.na(years_clean)] <- ''  # Replace years with no entries with empty string



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


##  Create Document Term Matrices ----

months_dtm <- tidy_months %>%
  cast_dtm(Month, word, n)  # Converts to document term matrix


##  Create Wordcloud containing most frequent words for the entire text ----

num_years <- dim(years_clean)[1]  # Number of years in the data set

entire_text <- ''  # Initialise empty string

for (i in 1:num_years) {  # Combine all entries into one string
  
  entire_text <- paste(entire_text, years_clean[i,2], sep = ' ')
  
}

entire_text_lower <- tolower(entire_text)  # Convert text to lowercase

entire_text_df <- tibble(Text = entire_text)  # Create tibble with with 1 row & column giving all text

tidy_text <- entire_text_df %>%
  unnest_tokens(word, Text) %>%  # Convert dataframe to one row per word
  anti_join(stop_words2) %>%  # Remove stopwords
  mutate(word = singularize(word)) %>%  # Singularise words
  mutate_if(is.character, str_replace_all, abbrevs) %>%  # Replace abbreviations
  count(word, sort = TRUE)  # Count frequency of each word per document

tidy_text_subset <- head(tidy_text, 100)  # Take subset containing most frequent words

# Create wordcloud containing most frequent words:

set.seed(1234)

ggplot(tidy_text_subset, aes(label = word, size = n)) +
  geom_text_wordcloud() +
  scale_size_area(max_size = 15) + 
  theme_minimal()


##  n-gram Frequencies (Politics) ----

politics_count <- tidy_months_text %>%
  mutate(s1 = str_count(Text, pattern = "(\\bbilly hughes\\b|\\bmr hughes\\b|\\bwm hughes\\b|\\bw m hughes\\b|\\bbillie hughes\\b|\\bwilliam hughes\\b|\\bprime minister\\b)")) %>%
  mutate(s2 = str_count(Text, pattern = "(\\bvote\\b|\\bvoting\\b)")) %>%
  mutate(s3 = str_count(Text, pattern = "(\\bconscription\\b)"))

politics <- politics_count %>% 
  dplyr::select(-Text) %>% 
  gather('n-gram', 'Frequency', s1:s3) %>% 
  group_by(`n-gram`) %>%
  arrange(Month) %>%
  mutate(MA = rollmean(Frequency, k = 3, fill = NA))

politics <- politics %>% filter(Month < 105)

ggplot(politics, aes(x = Month, y = Frequency, color = `n-gram`)) +
  geom_line() +
  scale_x_continuous(minor_breaks = 1:108, breaks = c(1,13,25,37,49,61,73,85,97,108), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Dec 1922')) +
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                        colour = "grey"), 
        panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                        colour = "white")) +
  xlab('\n Month') +
  ylab('Frequency \n') +
  scale_color_discrete(name = 'n-gram', labels = c("Billy Hughes", "Vote", "Conscription")) +
  theme(legend.position = c(0.85, 0.7))

##  n-gram Frequencies (Health) ----


health1_count <- tidy_months_text %>%
  mutate(s1 = str_count(Text, pattern = "(\\binfluenza\\b|\\flu\\b|\\bgrippe\\b)")) %>%
  mutate(s2 = str_count(Text, pattern = "(\\bspanish flu\\b|\\bspanish influenza\\b|\\bspanish grippe\\b)")) %>%
  mutate(s3 = str_count(Text, pattern = "(\\bsick\\b|\\bsickness\\b|\\bill\\b|\\billness\\b)")) %>%
  mutate(s4 = str_count(Text, pattern = "(\\bmedical\\b|\\bmedicine\\b)")) %>%
  mutate(s5 = str_count(Text, pattern = "(\\bfirst aid\\b)"))

health1 <- health1_count %>% 
  dplyr::select(-Text) %>% 
  gather('n-gram', 'Frequency', s1:s3) 

health1 <- health1 %>% filter(Month < 105)

ggplot(health1, aes(x = Month, y = Frequency, color = `n-gram`)) +
  geom_line() +
  scale_x_continuous(minor_breaks = 1:108, breaks = c(1,13,25,37,49,61,73,85,97,108), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Dec 1922')) +
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                        colour = "grey"), 
        panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                        colour = "white")) +
  xlab('\n Month') +
  ylab('Frequency \n') +
  scale_color_discrete(name = 'n-gram', labels = c("Flu", "Spanish Flu", "Sick", "Medical", "First Aid"))+
  theme(legend.position = c(0.85, 0.7))

health2_count <- tidy_months_text %>%
  mutate(s1 = str_count(Text, pattern = "(\\bdoctor\\b|\\bphysician\\b|\\bdoc\\b)")) %>%
  mutate(s2 = str_count(Text, pattern = "(\\bnurse\\b)")) %>%
  mutate(s3 = str_count(Text, pattern = "(\\bdentist\\b)")) %>%
  mutate(s5 = str_count(Text, pattern = "(\\bstretcher bearer\\b)"))

health2 <- health2_count %>% 
  dplyr::select(-Text) %>% 
  gather('n-gram', 'Frequency', s1:s5)  %>%
  group_by(`n-gram`) %>%
  arrange(Month) %>%
  mutate(MA = rollmean(Frequency, k = 3, fill = NA))

health2 <- health2 %>% filter(Month < 105)

ggplot(health2, aes(x = Month, y = Frequency, color = `n-gram`)) +
  geom_line() +
  scale_x_continuous(minor_breaks = 1:108, breaks = c(1,13,25,37,49,61,73,85,97,108), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Dec 1922')) +
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                        colour = "grey"), 
        panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                        colour = "white")) +
  xlab('\n Month') +
  ylab('Frequency \n') +
  scale_color_discrete(name = 'n-gram', labels = c("Doctor", "Nurse", "Dentist", "Stretcher Bearer")) +
  theme(legend.position = c(0.85, 0.7))

##  Tf-idf (Years) ----

# Create a dataframe where 1920, 1921, 1922 & 1923 are combined as one:

years_combined <- years_clean

years_combined$Year[years_combined$Year == 1921] <- 1920
years_combined$Year[years_combined$Year == 1922] <- 1920
years_combined$Year[years_combined$Year == 1923] <- 1920

years_tfidf <- years_combined %>%
  unnest_tokens(word, Text) %>%  # Convert dataframe to one row per word
  anti_join(stop_words2) %>%  # Remove stopwords
  mutate(word = singularize(word)) %>%  # Singularise words
  mutate_if(is.character, str_replace_all, abbrevs) %>%  #
  count(Year, word, sort = TRUE) %>% # Count frequency of each word per document
  bind_tf_idf(word, Year, n)  # Determine tf, idf and tfidf scores

years_tfidf %>%  ## Tfidf plot - top 20 words for given year
  filter(Year == 1920) %>%
  arrange(desc(tf_idf)) %>%
  mutate(word = factor(word, levels = rev(unique(word)))) %>% 
  group_by(Year) %>% 
  top_n(30) %>% 
  head(30) %>%
  ungroup() %>%
  ggplot(aes(word, tf_idf, fill = Year)) +
  geom_col(show.legend = FALSE) +
  labs(x = NULL, y = "tf-idf") +
  facet_wrap(~Year, ncol = 2, scales = "free") +
  coord_flip()


##  Determine Number of Topics ----  

result <- FindTopicsNumber(
  months_dtm,
  topics = seq(from = 2, to = 30, by = 1),
  metrics = c("Griffiths2004", "CaoJuan2009", "Arun2010", "Deveaud2014"),
  method = "Gibbs",
  control = list(seed = 1915),
  mc.cores = 2L,
  verbose = TRUE
)

FindTopicsNumber_plot(result)

ggsave('topic_num_1915.eps', plot = last_plot(), width = 22, height = 12, units = "cm")

##  Perform LDA and save results ----

months_lda <- topicmodels::LDA(months_dtm, k = 10, method = "Gibbs", control = list(seed = 1915))  # Perform LDA

months_topics <- tidy(months_lda, matrix = "beta")  # Get word probabilities for each topic

months_documents <- tidy(months_lda, matrix = "gamma")  # Get topic probabilities for each document

months_documents <- type_convert(months_documents)  # Convert document column to integers

# Create Tex Tables containing top 99 words for each topic

for (i in 1:10) {
  
  m_top_1 <- months_topics %>% filter(topic == i) %>% arrange(desc(beta)) %>% select(-topic) %>% head(n = 99)
  m_top_1 <- m_top_1 %>% add_column(rank = 1:99, .before = "term")
  m1 <- m_top_1 %>% filter(rank <= 33)
  m2 <- m_top_1 %>% filter(rank >= 34) %>% filter(rank <= 66)
  m3 <- m_top_1 %>% filter(rank >= 67) %>% filter(rank <= 99)
  
  m1['rank2'] <- m2$rank
  m1['term2'] <- m2$term
  m1['beta2'] <- m2$beta
  m1['rank3'] <- m3$rank
  m1['term3'] <- m3$term
  m1['beta3'] <- m3$beta
  
  cptn <- paste("Top 99 terms for Topic", as.character(i), "with their probabilities.", sep = " ")
  lbl <- paste("topic_", as.character(i), "_terms_(1915)", sep = "")
  fn <- paste(lbl, ".tex", sep = "")
  
  print(xtable(m1, type = "latex", caption = cptn, label = lbl, digits=c(0,0,0,4,0,0,4,0,0,4)), file = fn, include.rownames = FALSE)
  
}

# Create Plot of Topic Proportions over time:

m_docs <- months_documents %>% filter(document < 105)  # Only keep until end of 1922

m_docs$topic <- as.character(m_docs$topic)  # Convert topic column to character variables

topic_1 <- m_docs %>% filter(topic == 1) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_2 <- m_docs %>% filter(topic == 2) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_3 <- m_docs %>% filter(topic == 3) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_4 <- m_docs %>% filter(topic == 4) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_5 <- m_docs %>% filter(topic == 5) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_6 <- m_docs %>% filter(topic == 6) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_7 <- m_docs %>% filter(topic == 7) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_8 <- m_docs %>% filter(topic == 8) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_9 <- m_docs %>% filter(topic == 9) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))
topic_10 <- m_docs %>% filter(topic == 10) %>% arrange(document) %>% mutate(MA = rollmean(gamma, k = 5, fill = NA))

m_docs <- full_join(topic_1, topic_2)
m_docs <- full_join(m_docs, topic_3)
m_docs <- full_join(m_docs, topic_4)
m_docs <- full_join(m_docs, topic_5)
m_docs <- full_join(m_docs, topic_6)
m_docs <- full_join(m_docs, topic_7)
m_docs <- full_join(m_docs, topic_8)
m_docs <- full_join(m_docs, topic_9)
m_docs <- full_join(m_docs, topic_10)

m_docs$topic <- fct_recode(
  
  m_docs$topic,
  "Everyday Life" = "2",
  "Gallipoli" = "3",
  "Home Again" = "10",
  "Egypt" = "7",
  "Trenches (Middle)" = "8",
  "Trenches (Begin)" = "4",
  "War at Sea" = "9",
  "After the Armistice" = "1",
  "White Christmas" = "6",
  "Trenches (End)" = "5",
  
)

m_docs$topic <- factor(m_docs$topic, levels = c('Everyday Life', 'War at Sea', 'Egypt', 'Gallipoli', 'Trenches (Begin)', 'Trenches (Middle)', 'Trenches (End)', 'White Christmas', 'After the Armistice', 'Home Again'))

ggplot(m_docs, aes(document, MA, color = topic)) + 
  geom_line() +
  scale_x_continuous(minor_breaks = 1:108, breaks = c(1,13,25,37,49,61,73,85,97,108), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Dec 1922')) + 
  ylab('Probability \n') +
  xlab("\n Month") +
  scale_color_manual(values = c("#0085ff", "#8c04ec", "#ec0404", "#ec7904", "#042bec", "#ff00e7", "#fd5151", "#00ff85", "#005e78", "#03b834")) +
  theme_bw() + theme(panel.border = element_blank(), 
                     #axis.line = element_line(colour = "black"), 
                     axis.text.x = element_text(angle = 90))#,
legend.title = element_text(color = "black", size = 10),
legend.text = element_text(color = "black", size = 8))
#legend.position = "bottom")#,
#panel.grid.major = element_line(size = 0.5, linetype = 'solid',
colour = "grey"), 
# panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
colour = "white"))




ggsave('Topic_Modelling_1915_White.eps', plot = last_plot(), width = 20, height = 11, units = "cm")

## Sentiment Analysis ----

tidy_months_SA <- months_clean %>%
  unnest_tokens(word, Text) %>%  # Convert dataframe to one row per word
  mutate(word = singularize(word)) %>%  # Singularise words
  mutate_if(is.character, str_replace_all, abbrevs) %>%  # Replace abbreviations
  count(Month, word, sort = TRUE)  # Count frequency of each word per document


ww1_words <- unique(tidy_months_SA$word)

num_ww1_words <- length(ww1_words)

# AFINN ----

afinn <- get_sentiments("afinn")  # AFINN dictionary

afinn <- afinn %>% mutate(value = (((value + 5)/(5+5))*(1+1)-1))

afinn_words <- afinn$word

afinn_num <- sum(1*(afinn_words%in% ww1_words))

afinn_per <- afinn_num/num_ww1_words

sentiments_afinn <- tidy_months_SA %>% 
  inner_join(afinn)

sentiments_afinn$nsent <- sentiments_afinn$n * sentiments_afinn$value

sentiments_afinn <- sentiments_afinn %>% filter(nsent != 0)

sentiments_afinn <- sentiments_afinn %>%   
  group_by(Month) %>%  
  summarise(s = sum(nsent)/sum(n))

afinn_MA <- sentiments_afinn %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA)) 

afinn_MA$Dict <- 'AFINN'

sentiment_scores <- afinn_MA

# ANEW ----

anew <- read_csv("D:/Analysing-WW1-Diaries-Code/ANEW.csv")

anew_simplified <- anew %>% dplyr::select(Description, `Valence Mean`) %>% rename(word = Description, sentiment = `Valence Mean`)

anew_simplified <- anew_simplified %>% mutate(sentiment = (((sentiment - 1)/(9-1))*(1+1)-1))

anew_words <- anew_simplified$word

anew_num <- sum(1*(anew_words%in% ww1_words))

anew_per <- anew_num/num_ww1_words

sentiments <- tidy_months_SA %>% 
  inner_join(anew_simplified)

sentiments$nsent <- sentiments$n * sentiments$sentiment

sentiments <- sentiments %>% filter(nsent != 0)

sentiments <- sentiments %>% 
  group_by(Month) %>% 
  summarise(s = sum(nsent)/sum(n), n2 = sum(n))

anew_MA <- sentiments %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

anew_MA$Dict <- 'ANEW'

sentiment_scores <- sentiment_scores %>% add_row(Month = anew_MA$Month, s = anew_MA$s, MA = anew_MA$MA, Dict = anew_MA$Dict)

#sentiment_all <- anew_MA %>% dplyr::select(Month, s) %>% rename(ANEW = s)
#sentiment_MA <- anew_MA %>% dplyr::select(Month, MA) %>% rename(ANEW = MA)

#temp_s <- afinn_MA  %>% dplyr::select(Month, s) %>% rename(AFINN = s)
#temp_MA <- afinn_MA %>% dplyr::select(Month, MA) %>% rename(AFINN = MA)

#sentiment_all <- full_join(sentiment_all, temp_s)
#sentiment_MA <- full_join(sentiment_MA, temp_MA)




#sentiment_all <- sentiment_all %>% add_row(Month = 1, ANEW = NA, AFINN = NA, .before = 1)
#sentiment_MA <- sentiment_MA %>% add_row(Month = 1, ANEW = NA, AFINN = NA, .before = 1)

# SENTIWORD ----

data(hash_sentiment_sentiword)

sentiword <- as_tibble(hash_sentiment_sentiword)

sentiword <- sentiword %>% rename(word = x, value = y)

senti_words <- sentiword$word

senti_num <- sum(1*(senti_words%in% ww1_words))

senti_per <- senti_num/num_ww1_words

sentiments_senti <- tidy_months_SA %>%
  inner_join(sentiword)


sentiments_senti$nsent <- sentiments_senti$n * sentiments_senti$value

sentiments_senti <- sentiments_senti %>% filter(nsent != 0)

sentiments_senti <- sentiments_senti %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


sentiword_MA <- sentiments_senti %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

sentiword_MA$Dict <- 'SentiWordNet'

sentiment_scores <- sentiment_scores %>% add_row(Month = sentiword_MA$Month, s = sentiword_MA$s, MA = sentiword_MA$MA, Dict = sentiword_MA$Dict)


# HULIU ----

data(hash_sentiment_huliu)
huliu <- as_tibble(hash_sentiment_huliu)

huliu <- huliu %>% rename(word = x, value = y)

huliu$value[huliu$value == -2] <- -1

huliu_words <- huliu$word

huliu_num <- sum(1*(huliu_words%in% ww1_words))

huliu_per <- huliu_num/num_ww1_words

sentiments_huliu <- tidy_months_SA %>%
  inner_join(huliu)


sentiments_huliu$nsent <- sentiments_huliu$n * sentiments_huliu$value

sentiments_huliu <- sentiments_huliu %>% filter(nsent != 0)

sentiments_huliu <- sentiments_huliu %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


huliu_MA <- sentiments_huliu %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

huliu_MA$Dict <- 'Huliu'

sentiment_scores <- sentiment_scores %>% add_row(Month = huliu_MA$Month, s = huliu_MA$s, MA = huliu_MA$MA, Dict = huliu_MA$Dict)



# JOckers ----

jockers <- as_tibble(hash_sentiment_jockers)

jockers <- jockers %>% rename(word = x, value = y)

jockers_words <- jockers$word

jockers_num <- sum(1*(jockers_words%in% ww1_words))

jockers_per <- jockers_num/num_ww1_words

sentiments_jockers <- tidy_months_SA %>%
  inner_join(jockers)


sentiments_jockers$nsent <- sentiments_jockers$n * sentiments_jockers$value

sentiments_jockers <- sentiments_jockers %>% filter(nsent != 0)

sentiments_jockers <- sentiments_jockers %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


jockers_MA <- sentiments_jockers %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

jockers_MA$Dict <- 'Syuzhet'

sentiment_scores <- sentiment_scores %>% add_row(Month = jockers_MA$Month, s = jockers_MA$s, MA = jockers_MA$MA, Dict = jockers_MA$Dict)



# MCDONALD ----

data(hash_sentiment_loughran_mcdonald)
mcdonald <- as_tibble(hash_sentiment_loughran_mcdonald)

mcdonald <- mcdonald %>% rename(word = x, value = y)

mcdonald_words <- mcdonald$word

mcdonald_num <- sum(1*(mcdonald_words%in% ww1_words))

mcdonald_per <- mcdonald_num/num_ww1_words

sentiments_mcdonald <- tidy_months_SA %>%
  inner_join(mcdonald)


sentiments_mcdonald$nsent <- sentiments_mcdonald$n * sentiments_mcdonald$value

sentiments_mcdonald <- sentiments_mcdonald %>% filter(nsent != 0)

sentiments_mcdonald <- sentiments_mcdonald %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


mcdonald_MA <- sentiments_mcdonald %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

mcdonald_MA$Dict <- 'Loughran-Mcdonald'

sentiment_scores <- sentiment_scores %>% add_row(Month = mcdonald_MA$Month, s = mcdonald_MA$s, MA = mcdonald_MA$MA, Dict = mcdonald_MA$Dict)



# SenticNet ----

data("hash_sentiment_senticnet")
sentic <- as_tibble(hash_sentiment_senticnet)

sentic <- sentic %>% rename(word = x, value = y)

sentic_words <- sentic$word

sentic_num <- sum(1*(sentic_words%in% ww1_words))

sentic_per <- sentic_num/num_ww1_words

sentiments_sentic <- tidy_months_SA %>%
  inner_join(sentic)


sentiments_sentic$nsent <- sentiments_sentic$n * sentiments_sentic$value


sentiments_sentic <- sentiments_sentic %>% filter(nsent != 0)

sentiments_sentic <- sentiments_sentic %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


sentic_MA <- sentiments_sentic %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

sentic_MA$Dict <- 'SenticNet'

sentiment_scores <- sentiment_scores %>% add_row(Month = sentic_MA$Month, s = sentic_MA$s, MA = sentic_MA$MA, Dict = sentic_MA$Dict)



# NRC ----

data("hash_sentiment_nrc")
nrc <- as_tibble(hash_sentiment_nrc)

nrc <- nrc %>% rename(word = x, value = y)

nrc_words <- nrc$word

nrc_num <- sum(1*(nrc_words%in% ww1_words))

nrc_per <- nrc_num/num_ww1_words

sentiments_nrc <- tidy_months_SA %>%
  inner_join(nrc)


sentiments_nrc$nsent <- sentiments_nrc$n * sentiments_nrc$value

sentiments_nrc <- sentiments_nrc %>% filter(nsent != 0)

sentiments_nrc <- sentiments_nrc %>% 
  group_by(Month) %>%
  summarise(s = sum(nsent)/sum(n))


nrc_MA <- sentiments_nrc %>% arrange(Month) %>% mutate(MA = rollmean(s, k = 5, fill = NA))

nrc_MA$Dict <- 'NRC'

sentiment_scores <- sentiment_scores %>% add_row(Month = nrc_MA$Month, s = nrc_MA$s, MA = nrc_MA$MA, Dict = nrc_MA$Dict)


## Av ----

sentiment_scores2 <- sentiment_scores %>% filter(Month<105)  ######

ggplot(sentiment_scores2, aes(Month, MA, color = Dict)) + geom_line() +
  scale_x_continuous(minor_breaks = 1:108, breaks = c(1,13,25,37,49,61,73,85,97,108), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Dec 1922')) +
  labs(color = "Dictionary") +
  xlab("\n Month") +
  ylab("Sentiment Score \n")+ 
  theme_bw() +
  theme(panel.border = element_blank(), 
        # axis.line = element_line(colour = "black"), 
        axis.text.x = element_text(angle = 90))#,
legend.title = element_text(color = "black", size = 10),
legend.text = element_text(color = "black", size = 8))



av1 <- sentiment_scores %>%
  group_by(Month) %>%
  summarise(Av = mean(s))

sent_av <- av1 %>% arrange(Month) %>% mutate(MA = rollmean(Av, k = 5, fill = NA))


sent_av2 <- sent_av %>% filter(Month<105)

sent_all <- sentiment_scores %>% add_row(Month = av1_MA$Month, s = av1_MA$Av, MA = av1_MA$MA, Dict = 'Average')


sent_av3 <- sent_av2 %>% filter(Month <= 72) %>% filter(Month >= 8)

ggplot(sent_av3, aes(Month, MA)) + geom_line() +
  scale_x_continuous(minor_breaks = 1:72, breaks = c(1,13,25,37,49,61,72), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Dec 1919'), limits=c(1, 72)) +
  scale_y_continuous(limits=c(0, 0.2)) +
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                        colour = "grey"), 
        panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                        colour = "white")) +
  xlab("\n Month") +
  ylab("Average Sentiment Score \n")


m_docs3 <- m_docs %>% 
  dplyr::select(-MA) %>%
  mutate(gam = (gamma*0.2)/0.5 - 0.0) %>%
  group_by(topic) %>%
  mutate(MA = rollmean(gam, k = 5, fill = NA)) %>%
  ungroup() %>%
  filter(document <= 72) %>% 
  filter(document >= 8) %>% 
  filter(topic != 'Everyday Life') %>% 
  filter(topic != 'Home Again')

ggplot(m_docs3, aes(x = document)) +
  geom_line(aes(y=MA, color = topic, linetype = 'solid')) +
  geom_line(sent_av3, mapping = aes(x = Month, y = MA, linetype = "dashed"), colour ="black")  +
  scale_y_continuous(name="Average Sentiment Score \n", sec.axis=sec_axis(~./(0.2/0.5), name="Topic Probability \n")) +
  xlab("\n Month") +
  scale_color_manual(values = c("#8c04ec", "#ec0404", "#ec7904", "#042bec", "#ff00e7", "#fd5151", "#00ff85", "#005e78"), name = "Topic")+
  scale_x_continuous(minor_breaks = 1:72, breaks = c(1,13,25,37,49,61,72), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Dec 1919'), limits=c(1, 72)) + 
  theme(axis.text.x = element_text(angle = 90),
        panel.grid.major = element_line(size = 0.5, linetype = 'solid',
                                        colour = "grey"), 
        panel.grid.minor = element_line(size = 0.25, linetype = 'solid',
                                        colour = "white")) +
  scale_linetype_manual(
    values = c(2,1), # play with the numbers to get the correct styling
    name = "Linetype",
    labels = c('Av. Sentiment Score', 'Topic Probability')
    
    
    
    ## Num words per day ----
    
    num_word_days <- days_clean %>%
      group_by(Date) %>%
      summarise(n = wordcount(Text, sep = " ", count.function = sum))
    
    num_word_months <- months_clean %>%
      group_by(Month) %>%
      summarise(n = wordcount(Text, sep = " ", count.function = sum))
    
    ggplot(num_word_months, aes(x = Month, y = n)) + 
      geom_col(color = "black", fill = "steelblue") +
      ylab("Number of Words \n") +
      xlab("\n Month") +
      scale_x_continuous(minor_breaks = 1:120, breaks = c(1,13,25,37,49,61,73,85,97,109,120), labels = c('Jan 1914', 'Jan 1915', 'Jan 1916', 'Jan 1917', 'Jan 1918', 'Jan 1919', 'Jan 1920', 'Jan 1921', 'Jan 1922', 'Jan 1923', 'Dec 1923')) + 
      theme(axis.text.x = element_text(angle = 90))# + 
    theme_bw() + theme(panel.border = element_blank(), 
                       #axis.line = element_line(colour = "black"), 
                       axis.text.x = element_text(angle = 90))
    
    
    ggsave('Num_Words_Months.eps', plot = last_plot(), width = 15, height = 10, units = "cm")
    
    
    