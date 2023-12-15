# Load the tidyverse package
library(tidyverse)
library(here)

# Automatically set the working directory to the project's top-level directory
setwd(paste0(here(),"/AALL_Behavioral_Testing_Analysis"))

# List all files that start with "Test" and end with ".csv"
files <- list.files(pattern = "^Test.*\\.csv$")

# Read each file, add a column for the filename, extract ID, and combine into a single dataframe
combined_data <- map_dfr(files, function(file) {
  read_csv(file) %>%
    mutate(FileName = file,
           ID = str_extract(file, "(?<=_)\\d{3}(?=\\.csv)"))
})

# Compute subject level data, including both overall accuracy and accuracy by block
data_subj_raw = combined_data %>%
  group_by(ID, block) %>%
  summarise(acc_block = mean(Accuracy, na.rm = TRUE)) %>%
  ungroup() %>%
  spread(key = block, value = acc_block) %>%
  rename(block_1 = `1`, block_2 = `2`, block_3 = `3`, block_4 = `4`) %>%
  rowwise() %>%
  mutate(acc_overall = mean(c(block_1, block_2, block_3, block_4),na.rm = TRUE)) %>%
  mutate(acc_last3blocks = mean(c(block_2, block_3, block_4),na.rm = TRUE)) %>%
  mutate(trial_num = 48) %>%
  mutate(binom_test_p_value = round(binom.test(round(acc_last3blocks * trial_num), trial_num, p = 0.5)$p.value, digits = 3))  

# Conduct binomial test based on the last three blocks


# Set excluded subject id pool

# Compile final included subjects

# Plot accuracy and RT overall

# Plot accuracy and RT by block

# Running LMM models

