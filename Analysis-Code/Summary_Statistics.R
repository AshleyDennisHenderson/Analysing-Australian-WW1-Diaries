
# This code creates the tables and graphs for Section 3.5 of my Masters Thesis (Summary Statistics)
#
# Ashley Dennis-Henderson

##  Load Packages ----

pacman::p_load(tidyverse, plotrix, readtext, data.table, tidytext, tolerance)

setwd("D:/WW1_Diaries")  # Set Working Directory

##  Load Metadata ----

metadata <- read.csv('/WW1_Diaries/Cleaned Data 1i - V1/metadata.csv')  # Load Metadata

metadata <- metadata %>% 
  dplyr::select(-Document.Name, -Original.Title, -Item.Number, -Start.Month, -Start.Year, -End.Month, -End.Year, -Receiver, -Regarding, -Node, -Duplicate)  # Remove unneccessary columns


##  Create Zipf Graph ----

df <- read_csv('/WW1_Diaries/Data_Sorted_by_Type.csv')


book_words <- df %>%
  unnest_tokens(word, text) %>%
  count(Type, word, sort = TRUE)

total_words <- book_words %>% 
  group_by(Type) %>% 
  summarize(total = sum(n))

book_words <- left_join(book_words, total_words)

freq_by_rank <- book_words %>% 
  group_by(Type) %>% 
  mutate(rank = row_number(), 
         `term frequency` = n/total)

f <- exp(-1.539647) / (freq_by_rank$rank+1.550628)^(1.060630)

freq_by_rank %>% 
  ggplot(aes(rank, `term frequency`, color = Type)) + 
  geom_line(size = 1, show.legend = TRUE)+ 
  geom_abline(mapping = aes(intercept = 0.9024, slope = -1.5929, linetype = 'dashed'),  color = "gray50", size = 1) + 
  geom_line(mapping = aes(x = rank, y = f, linetype = "dotdash"), color = "gray50", size = 1) +
  scale_x_log10() +
  scale_y_log10() + 
  scale_linetype_manual(
    values = c(2,4), # play with the numbers to get the correct styling
    name = "Linetype",
    labels = c('Zipf', 'Zipf-Mandelbrot')
  ) +
  ylab('log(Term Frequency) \n') +
  xlab('\n log(Rank)')

ggsave('zipf.eps', plot = last_plot(), width = 15, height = 10, units = "cm")



## Mandelbrot ----

N <- max(f_diary$rank) # Num unique words
M <- sum(f_diary$`term frequency`)  # total num words

q0 <- 0; s0 <- 1  # intial guesses

mandel <- function(r, N, q, s) {
  
  k <- 1:N
  
  H <- sum(1/(k+q)^s)
  
  y <- (1/H)/(r+q)^s
  
  return(y)
  
}

funct <- function(r, M, N, f, x) {
  
 x <- sum( (M*mandel(r, N, x[1], x[2]) - f)^2)
 
 return(x)
  
}

o <- optim(c(q0,s0), fn = funct, r = f_diary$rank, M = M, N = N, f = f_diary$`term frequency`)


##  Create Summary Table of Number of Pages, Words and Authors for Each Type of Document ----

Num_Authors_diary <- metadata %>%  # Determine Number of Distinct Authors for Diaries
  filter(Document.Type == 'diary') %>%
  dplyr::select(Author.First.Name, Author.Last.Name) %>%
  distinct() %>%
  count()

Num_Authors_letter <- metadata %>%  # Determine Number of Distinct Authors for Letters
  filter(Document.Type == 'letter') %>%
  dplyr::select(Author.First.Name, Author.Last.Name) %>%
  distinct() %>%
  count()

Num_Authors_letter_diary <- metadata %>%  # Determine Number of Distinct Authors for Letter-Diaries
  filter(Document.Type == 'letter diary') %>%
  dplyr::select(Author.First.Name, Author.Last.Name) %>%
  distinct() %>%
  count()

Num_Authors_narrative <- metadata %>%  # Determine Number of Distinct Authors for War Narratives
  filter(Document.Type == 'narrative') %>%
  dplyr::select(Author.First.Name, Author.Last.Name) %>%
  distinct() %>%
  count()

Num_Authors_other <- metadata %>%  # Determine Number of Distinct Authors for Other
  filter(Document.Type == 'other') %>%
  dplyr::select(Author.First.Name, Author.Last.Name) %>%
  distinct() %>%
  count()

Num_Authors <- c(Num_Authors_diary$n[1], Num_Authors_letter$n[1], Num_Authors_letter_diary$n[1], Num_Authors_narrative$n[1], Num_Authors_other$n[1])  # Combine the Number of Authors per type into a single list

overall_summary <- metadata %>%  # For each document type determine how many there are, the number of pages and number of words
  group_by(Document.Type) %>%
  summarise(Number = n(), Num.Pages = sum(Number.of.Pages), Num.Words = sum(Number.of.Words))

overall_summary$Num.Authors <- Num_Authors  # Add the number of authors per document type to our summary


##  ----

metadata_diaries <- metadata %>% filter(Document.Type == 'diary')  # Filter for only diaries

metadata_diaries <- metadata_diaries %>% filter(Number.of.Pages > 0)  # Filter for non-empty diaries

results2 <- metadata_diaries %>%
  dplyr::select(Author.First.Name, Author.Last.Name, Number.of.Pages, Number.of.Words)

r3 <- results2 %>%
  group_by(Author.First.Name, Author.Last.Name) %>%
  summarise(num_pages = sum(Number.of.Pages), num_words = sum(Number.of.Words))

r <- results2 %>% dplyr::select(Author.First.Name, Author.Last.Name) %>%
  group_by_all %>% count

ggplot(r, aes(x = n)) + 
  geom_histogram(color="black", fill = "steelblue", binwidth = 1) +
  xlab('\n Number of Diaries') +
  ylab('Number of Authors \n') + 
  annotate(geom="text", x=25, y=24, label="Aubrey \n Wiltshire", color="red") +
  geom_segment(aes(x = 25, y = 13, xend = 26, yend = 3, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE) + 
  annotate(geom="text", x=16, y=24, label="Archie \n Barwick", color="red") +
  geom_segment(aes(x = 16, y = 13, xend = 16, yend = 3, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE)



ggsave('histogram_num_authors_diaries.eps', plot = last_plot(), device = 'eps', width = 15, height = 7, units = "cm")

# results3 <- results2 %>%
#   group_by(Document.Type) %>%
#   summarise(n())
summary_authors_diaries <- summary(r$n)  # Summary

ggplot(r3, aes(x = num_pages)) + 
  geom_histogram(color="black", fill = "steelblue") +
  xlab('\n Number of Pages') +
  ylab('Number of Authors \n')  + 
  annotate(geom="text", x=2100, y=24, label="Aubrey \n Wiltshire", color="red") +
  geom_segment(aes(x = 2100, y = 15, xend = 2450, yend = 2, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE) + 
  annotate(geom="text", x=2500, y=24, label="Archie \n Barwick", color="red") +
  geom_segment(aes(x = 2500, y = 15, xend = 2550, yend = 2, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE)


ggsave('histogram_num_authors_pages.eps', plot = last_plot(), device = 'eps', width = 15, height = 7, units = "cm")

summary_authors_pages <- summary(r3$num_pages)  # Summary

ggplot(r3, aes(x = num_words)) + 
  geom_histogram(color="black", fill = "steelblue") +
  xlab('\n Number of Words') +
  ylab('Number of Authors \n') + 
  annotate(geom="text", x=491000, y=23, label="Aubrey \n Wiltshire", color="red") +
  geom_segment(aes(x = 491000, y = 15, xend = 494500, yend = 2, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE) + 
  annotate(geom="text", x=393000, y=23, label="Archie \n Barwick", color="red") +
  geom_segment(aes(x = 393000, y = 15, xend = 393000, yend = 2, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE)


ggsave('histogram_num_authors_words.eps', plot = last_plot(), device = 'eps', width = 15, height = 7, units = "cm")

summary_authors_words <- summary(r3$num_words)  # Summary

summary_words <- summary(metadata_diaries$Number.of.Words)  # Summary of the number of words

summary_pages <- summary(metadata_diaries$Number.of.Pages)  # Summary of the number of pages

ggplot(metadata_diaries, aes(x = Number.of.Words)) +
  geom_histogram(color = "black", fill = "steelblue") + 
  xlab('\n Number of Words') + 
  ylab('Number of Diaries \n') + 
  annotate(geom="text", x=190000, y=30, label="Charles \n Rosenthal", color="red") +
  geom_segment(aes(x = 190000, y = 18, xend = 200000, yend = 3, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE)

ggsave('histogram_num_words.eps', plot = last_plot(), device = 'eps', width = 15, units = "cm")

ggplot(metadata_diaries, aes(x = Number.of.Pages)) +
  geom_histogram(color = "black", fill = "steelblue") + 
  xlab('\n Number of Pages') + 
  ylab('Number of Diaries \n') + 
  annotate(geom="text", x=500, y=20, label="Charles \n Rosenthal", color="red") +
  geom_segment(aes(x = 500, y = 15, xend = 505, yend = 3, colour = "red"), arrow = arrow(length = unit(0.03, "npc")), show.legend = FALSE)


ggsave('histogram_num_pages.eps', plot = last_plot(), device = 'eps', width = 15, units = "cm")



metadata2 <- metadata %>%
  dplyr::select(`Document.Type`, `Author.First.Name`, `Author.Last.Name`, `Number.of.Pages`, `Number.of.Words`)
