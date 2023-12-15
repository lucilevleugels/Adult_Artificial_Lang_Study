# Load the tidyverse package
library(tidyverse)
library(here)
library(afex)

# List all files that start with "Test" and end with ".csv"
files <- list.files(pattern = "^Test.*\\.csv$")

# Read each file, add a column for the filename, extract ID, and combine into a single dataframe
combined_data <- map_dfr(files, function(file) {
  read_csv(file) %>%
    mutate(FileName = file,
           ID = str_extract(file, "(?<=_)\\d{3}(?=\\.csv)"))
})

# There are two response time columns, something is wrong in the original experimental code, but combining them for now. 
combined_data = combined_data %>%
  mutate(rt = coalesce(`Response Time`, `Response_Time`))

# Compute subject level data, including both overall accuracy and accuracy by block
data_subj_raw = combined_data %>%
  group_by(ID, block) %>%
  summarise(acc_block = mean(Accuracy, na.rm = TRUE)) %>%
  ungroup() %>%
  spread(key = block, value = acc_block) %>%
  rename(block_1 = `1`, block_2 = `2`, block_3 = `3`, block_4 = `4`) %>%
  rowwise() %>%
  mutate(acc_overall = mean(c(block_1, block_2, block_3, block_4),na.rm = TRUE)) %>%
  mutate(acc_last2blocks = mean(c(block_3, block_4),na.rm = TRUE)) %>%
  mutate(trial_num = 24) %>%
  mutate(binom_test_p_value = round(binom.test(round(acc_last2blocks * trial_num), trial_num, p = 0.5)$p.value, digits = 3))  

# Set excluded subject id pool
# self-reported ADHD (who was not concentrated during the session): 018, 022, 042
# didn't follow instruction: 033
# perfect score from block1: 026
exclusion_session_comments = c("018", "022", "042", "033", "026")
exclusion_chance = data_subj_raw %>% filter(binom_test_p_value > 0.05) %>% pull(ID)
exclusion_ids = unique(c(exclusion_session_comments, exclusion_chance))
print(exclusion_ids)

# Compile final included subjects
data_trial = combined_data %>%
  filter(!ID %in% exclusion_ids) %>%
  mutate(ID = as.numeric(ID))

# Read in condition assignment file
condition_assignment = read.csv("ParticipantCOnditionKey_NoExclusions.csv") %>%
  rename(ID = Participant_ID) %>%
  select(ID, Condition)

data_trial = data_trial %>%
  left_join(condition_assignment, by = "ID") %>%
  mutate(condition_2levels = ifelse(Condition == "correlated", "correlated", "isolated")) # adding new condition assignment

# Get the number of participants for each condition
data_trial %>%
  group_by(condition_2levels) %>%
  summarise(number_of_unique_participants = n_distinct(ID))

  
# For 4 conditions contrast, compute subject level overall accuracy, RT, and se 
data_subj_overall = data_trial %>%
  group_by(ID, Condition) %>%
  summarise(acc_subj = mean(Accuracy, na.rm = TRUE), 
            rt_subj = median(rt, na.rm = TRUE))

data_condition_overall = data_subj_overall %>%
  group_by(Condition) %>%
  summarise(acc_group = mean(acc_subj, na.rm = TRUE),
            acc_group_se = sd(acc_subj)/sqrt(n()),
            rt_group = mean(rt_subj, na.rm = TRUE),
            rt_group_se = sd(rt_subj)/sqrt(n()))

# For 2 conditions contrast, compute subject level overall accuracy, RT, and se 
# Caution: RT probably should only be acc = 1 trials, so no plot on it now. 
data_subj_overall = data_trial %>%
  group_by(ID, condition_2levels) %>%
  summarise(acc_subj = mean(Accuracy, na.rm = TRUE), 
            rt_subj = median(rt, na.rm = TRUE))

data_condition_overall = data_subj_overall %>%
  group_by(condition_2levels) %>%
  summarise(acc_group = mean(acc_subj, na.rm = TRUE),
            acc_group_se = sd(acc_subj)/sqrt(n()),
            rt_group = mean(rt_subj, na.rm = TRUE),
            rt_group_se = sd(rt_subj)/sqrt(n()))

# For 2 conditions contrast, generate by block data
data_subj_by_block= data_trial %>%
  group_by(ID, condition_2levels, block) %>%
  summarise(acc_subj = mean(Accuracy, na.rm = TRUE), 
            rt_subj = median(rt, na.rm = TRUE))

data_condition_by_block = data_subj_by_block %>%
  group_by(condition_2levels, block) %>%
  summarise(acc_group = mean(acc_subj, na.rm = TRUE),
            acc_group_se = sd(acc_subj)/sqrt(n()),
            rt_group = mean(rt_subj, na.rm = TRUE),
            rt_group_se = sd(rt_subj)/sqrt(n()))


# Plot block data with error bars
ggplot(data_condition_by_block, aes(x = block, y = acc_group, group = condition_2levels, color = condition_2levels)) +
  geom_line() +
  geom_errorbar(aes(ymin = acc_group - acc_group_se, ymax = acc_group + acc_group_se), width = 0.1) +
  labs(x = "Block",
       y = "Accuracy",
       color = "Condition") +
  theme_bw(base_size = 11) +
  theme(panel.border = element_blank(), panel.grid.major = element_blank(),
                     panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"))

# Save the plot
ggsave("acc_by_block.png", width = 6, height = 4, dpi = 300)


# Running LMM models on trial level data--not enough people yet, but down the road
# make sure these columns are all factors
data_trial = data_trial %>%
  mutate(across(c(condition_2levels, ID, trial), as.factor))
  
mixed(Accuracy ~ condition_2levels + (1|ID) + (1|trial), data = data_trial, family = binomial, method = "LRT")

mixed(Accuracy ~ condition_2levels + (1|ID) + (1|trial), data = subset(data_trial, block != 4), family = binomial, method = "LRT")


