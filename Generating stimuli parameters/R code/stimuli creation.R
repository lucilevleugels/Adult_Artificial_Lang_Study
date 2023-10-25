######################### Generate learning data #######################
##### select 120 combos from the 720 non-repeating possibilities, for each block, set 20 for learning, 12 for testing.


# Load necessary libraries
library(combinat)
library(tidyverse)

# Set seed for reproducibility
set.seed(123)

# Define the pool of syllabus items
syllabus_pool <- c("barget", "bimdah", "chelad", "dingep", "fisslin", "goorshell", 
                   "haagle", "jeelow", "limeber", "makkot", "nellby", "pakrid", 
                   "rakken", "sumbark")

# Randomly select 10 items from the pool
selected_items <- sample(syllabus_pool, 10)

# Generate all possible permutations of the selected items
all_permutations <- expand.grid(selected_items, selected_items, selected_items)

# Filter out invalid permutations (those with repeated items)
valid_permutations <- all_permutations[all_permutations$Var1 != all_permutations$Var2 & 
                                         all_permutations$Var1 != all_permutations$Var3 & 
                                         all_permutations$Var2 != all_permutations$Var3, ]

# Randomly select 20 valid permutations for the dataframe
selected_permutations <- valid_permutations[sample(nrow(valid_permutations), 20), ]

# Construct the initial dataframe
df <- data.frame(
  trial = 1:20,
  item1 = selected_permutations$Var1,
  item2 = selected_permutations$Var2,
  item3 = selected_permutations$Var3
)

# Identify remaining items for case markers
remaining_items <- setdiff(syllabus_pool, selected_items)

# Randomly select 3 items to be used as case markers
casemarker_items <- sample(remaining_items, 3)

# Add case markers to the dataframe
df$casemarker1 <- rep(casemarker_items[1], nrow(df))
df$casemarker2 <- rep(casemarker_items[2], nrow(df))
df$casemarker3 <- rep(casemarker_items[3], nrow(df))

# Create a concatenated column for items and case markers
df$final <- paste(df$item1, df$casemarker1, df$item2, df$casemarker2, df$item3, df$casemarker3, sep = " ")

# Create a variation of the dataframe with swapped case markers for isolated condition
df_new <- df
swap_rows <- sample(1:nrow(df), nrow(df) * 0.5)  # Identify 50% of rows to swap
df_new$casemarker2[swap_rows] <- df$casemarker3[swap_rows]
df_new$casemarker3[swap_rows] <- df$casemarker2[swap_rows]
df_new$final <- paste(df_new$item1, df_new$casemarker1, df_new$item2, df_new$casemarker2, df_new$item3, df_new$casemarker3, sep = " ")

# Label the conditions
df$condition <- "correlated"
df_new$condition <- "isolated"

# Combine the original and new dataframes
combined_df <- rbind(df, df_new)

# Save the data to a csv file
write.csv(combined_df, "data_source.csv", row.names = FALSE)

######################### Generate testing data #######################---still working on this. 
##### generating foils (visual), they are two types of foil
#### type 1 (6 trial each block): transposition. for example: ABC, can be transposed into two way: BCA, CAB
#### type 2 (6 trial each block): one item change, for example: ABC can be paired with DBC (D is randomly chose from 10-3 = 7 possible symbols). 
#### There are a total of 3 possible changes (left place, middle, right place), creat two trials for each of the change

