import random
from itertools import permutations
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


def generate_transposition_foil(items,):
    

    cyclic_permutations = []

    for perm in permutations(items):
        cyclic_permutation = ','.join(perm)
        if cyclic_permutation not in cyclic_permutations:
            cyclic_permutations.append(cyclic_permutation)

    trans_foils = [[foil] for foil in cyclic_permutations[1:]]
    return trans_foils

# Set seed for reproducibility
random.seed(123)

# Define the pool of syllabus items
syllabus_pool = ["barget", "bimdah", "chelad", "dingep", "fisslin", "goorshell",
                 "haagle", "jeelow", "limeber", "makkot", "nellby", "pakrid",
                 "rakken", "sumbark"]

# Randomly select 10 items from the pool
selected_items = random.sample(syllabus_pool, 10)

# Generate all possible permutations of the selected items
all_permutations = list(permutations(selected_items, 3))

# Filter out invalid permutations (those with repeated items)
valid_permutations = [p for p in all_permutations if len(set(p)) == len(p)]

# Randomly select 20 valid permutations
selected_permutations = random.sample(valid_permutations, 20)

# Create the initial DataFrame
df = pd.DataFrame({
    'trial': range(1, 21),
    'item1': [p[0] for p in selected_permutations],
    'item2': [p[1] for p in selected_permutations],
    'item3': [p[2] for p in selected_permutations]
})

# Identify remaining items for case markers
remaining_items = list(set(syllabus_pool) - set(selected_items))

# Randomly select 3 items to be used as case markers
casemarker_items = random.sample(remaining_items, 3)

# Add case markers to the DataFrame
df['casemarker1'] = casemarker_items[0]
df['casemarker2'] = casemarker_items[1]
df['casemarker3'] = casemarker_items[2]

# Create a concatenated column for items and case markers
df['final'] = df['item1'] + " " + df['casemarker1'] + " " + df['item2'] + " " + df['casemarker2'] + " " + df['item3'] + " " + df['casemarker3']

# Create a new DataFrame with swapped case markers
df_new = df.copy()
swap_rows = random.sample(range(len(df)), int(len(df) * 0.5))  # Identify 50% of rows to swap
df_new.loc[swap_rows, ['casemarker2', 'casemarker3']] = df_new.loc[swap_rows, ['casemarker3', 'casemarker2']]
df_new['final'] = df_new['item1'] + " " + df_new['casemarker1'] + " " + df_new['item2'] + " " + df_new['casemarker2'] + " " + df_new['item3'] + " " + df_new['casemarker3']

# Label the conditions
df['condition'] = "correlated"
df_new['condition'] = "isolated"

# Combine the original and new DataFrames
combined_df = pd.concat([df, df_new], ignore_index=True)
# combined_df

print('saving train-csv')
combined_df.to_csv('train.csv',index=False)

## GENERATING TEST SET
test_cond_corr = combined_df[combined_df['condition']=='correlated']
test_cond_iso = combined_df[combined_df['condition']=='isolated']

test_cond_corr = test_cond_corr.sample(n=12).reset_index(drop=True)
test_cond_iso = test_cond_iso.sample(n=12).reset_index(drop=True)

test_df = pd.concat([test_cond_corr, test_cond_iso], axis=0).reset_index(drop=True)

# foil_categories
# Define the item categories
foil_category_1 = ['transposition']*6
foil_category_2 = ['itemchange']*6

foil_categories = foil_category_1 + foil_category_2 + foil_category_1 + foil_category_2
test_df['foil_category'] = foil_categories

test_df_transposition = test_df[test_df['foil_category']=='transposition']
test_df_itemchange = test_df[test_df['foil_category']=='itemchange']


# TRANSPOSITION
list_of_foils = []
print("Generating Transposition Foils.")
for row in test_df_transposition[['item1','item2','item3']].iterrows():
    target_items = row[1].to_list()
    trans_foils = generate_transposition_foil(target_items)
    trans_foils = [item[0].split(',') for item in trans_foils]
    transposition_foil = random.choice(trans_foils)
    list_of_foils.append(transposition_foil)
test_df_transposition['foil'] = list_of_foils

# ITEM CHANGE
print("Generating Item Change Foils.")
list_of_foils = []
for row in test_df_itemchange[['item1','item2','item3']].iterrows():
    target_items = row[1].to_list()
    ##print(target_items)
    possibilities =  list(set(selected_items) - set(target_items))
    #print(possibilities)
    item_change = random.choice(possibilities)
    positions = [0,1,2] # left, center, middle
    position_selection = random.choice(positions)
    #print(item_change)
    #print(position_selection)
    
    itemchange_foils = target_items
    itemchange_foils[position_selection] = item_change
    list_of_foils.append(itemchange_foils)
    
    
test_df_itemchange['foil'] = list_of_foils


# REORDERING 

test_df = pd.concat([test_df_transposition, test_df_itemchange],axis=0)
# reordering
corr_df = test_df[test_df['condition']=='correlated']
iso_df = test_df[test_df['condition']=='isolated']

final_test_df = pd.concat([corr_df,iso_df],axis=0)

print('saving test-csv')
final_test_df.to_csv('test.csv',index=False)

print('-'*25)
print('Job Completed!')




    




