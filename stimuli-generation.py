import random
from itertools import permutations
import pandas as pd
import os
import shutil
import warnings
import random
import numpy as np
from itertools import permutations

warnings.filterwarnings('ignore')


# Set seed for reproducibility
np.random.seed(123)

# create train and test directories 
# os.makedirs('./Train/', exist_ok=True)
# os.makedirs('./Test/', exist_ok=True)



def generate_transposition_foil(items,):
    

    cyclic_permutations = []

    for perm in permutations(items):
        cyclic_permutation = ','.join(perm)
        if cyclic_permutation not in cyclic_permutations:
            cyclic_permutations.append(cyclic_permutation)

    trans_foils = [[foil] for foil in cyclic_permutations[1:]]
    return trans_foils

# Function to swap case markers for a given row
def swap_case_markers(row, combination):
    if combination == "isolated-left":
        row['casemarker2'], row['casemarker3'] = row['casemarker3'], row['casemarker2']
    elif combination == "isolated-center":
        row['casemarker1'], row['casemarker3'] = row['casemarker3'], row['casemarker1']
    elif combination == "isolated-right":
        row['casemarker1'], row['casemarker2'] = row['casemarker2'], row['casemarker1']
    return row



def generate_training_conditions(valid_permutations, image_association):

    # Randomly select 20 valid permutations
    selected_permutations = random.sample(valid_permutations, 80)

    # Create the initial DataFrame
    df = pd.DataFrame({
        'trial': range(1, 81),
        'item1': [p[0] for p in selected_permutations],
        'item2': [p[1] for p in selected_permutations],
        'item3': [p[2] for p in selected_permutations]
    })

    # Identify remaining items for case markers
    remaining_items = list(set(syllabus_pool) - set(selected_items))

    # Randomly select 3 items to be used as case markers
    casemarker_items = random.sample(remaining_items, 3)

    # Randomly select 3 items to be used as case markers
    casemarker_items = random.sample(remaining_items, 3)

    # Add case markers to the DataFrame
    df['casemarker1'] = casemarker_items[0]
    df['casemarker2'] = casemarker_items[1]
    df['casemarker3'] = casemarker_items[2]

    # Create a list of case marker combinations
    case_marker_combinations = ["correlated", "isolated-left", "isolated-center", "isolated-right"]

    # Create an empty list to store rows
    rows = []

    # Create rows for each combination of case markers
    for combination in case_marker_combinations:
        # Create a new DataFrame with swapped case markers
        df_new = df.copy()
        
        
        
        # Identify 50% of rows to swap in df_new
        swap_rows = random.sample(range(len(df_new)), int(len(df_new) * 0.5))

        # Swap casemarkers in df_new for the identified rows
        for row in swap_rows:
            df_new.iloc[row] = swap_case_markers(df_new.iloc[row], combination)

        # Update the 'final' column in df_new
        df_new['final'] = df_new['item1'] + " " + df_new['casemarker1'] + " " + df_new['item2'] + " " + df_new['casemarker2'] + " " + df_new['item3'] + " " + df_new['casemarker3']

        # Label the conditions
        df_new['condition'] = combination
        
        rows.append(df_new)

    # Combine the DataFrames for different combinations
    combined_df = pd.concat(rows, ignore_index=True)

    # audio_sequences
    audio_sequences = []
    for row in combined_df[['item1','casemarker1','item2','casemarker2','item3','casemarker3']].iterrows():
        seq = [word+'.wav' for word in row[1].to_list()]
        audio_sequences.append(seq)
    

    combined_df['audio_sequence'] = audio_sequences

    # image sequence 
    image_sequence = []
    for row in combined_df[['item1','item2','item3']].iterrows():
        seq = [image_association[word] for word in row[1].to_list()]
        image_sequence.append(seq)

    combined_df['image_sequence'] = image_sequence

    print('Saving train-csv')
    combined_df.to_csv('./Data/train_v4.csv',index=False)
    print("Invididualising by condition")
    print("Saving files")
    for condition in combined_df['condition'].unique():
        print(f"- {condition}")
        combined_df[combined_df['condition']==condition].to_csv(f'./Data/{condition}_train.csv',index=False)

    return selected_permutations, remaining_items


def generate_test_conditions(valid_permutations, selected_permutations, remaining_items, image_association):

    # Randomly select 48 permutations from the remaining 20
    test_permutations = random.sample(list(set(valid_permutations) - set(selected_permutations)),48)

    # Create the test DataFrame
    test_df = pd.DataFrame({
        'trial': range(1, 49),
        'item1': [p[0] for p in test_permutations],
        'item2': [p[1] for p in test_permutations],
        'item3': [p[2] for p in test_permutations]
    })

    # Randomly select 3 items to be used as case markers
    casemarker_items = random.sample(remaining_items, 3)

    # Randomly select 3 items to be used as case markers
    casemarker_items = random.sample(remaining_items, 3)

    # Add case markers to the DataFrame
    test_df['casemarker1'] = casemarker_items[0]
    test_df['casemarker2'] = casemarker_items[1]
    test_df['casemarker3'] = casemarker_items[2]



    # Create a list of case marker combinations
    case_marker_combinations = ["correlated", "isolated-left", "isolated-center", "isolated-right"]

    # Create an empty list to store rows
    rows = []

    # Create rows for each combination of case markers
    for combination in case_marker_combinations:
        # Create a new DataFrame with swapped case markers
        df_new = test_df.copy()
        
       
        # Identify 50% of rows to swap in df_new
        swap_rows = random.sample(range(len(df_new)), int(len(df_new) * 0.5))

        # Swap casemarkers in df_new for the identified rows
        for row in swap_rows:
            df_new.iloc[row] = swap_case_markers(df_new.iloc[row], combination)

        # Update the 'final' column in df_new
        df_new['final'] = df_new['item1'] + " " + df_new['casemarker1'] + " " + df_new['item2'] + " " + df_new['casemarker2'] + " " + df_new['item3'] + " " + df_new['casemarker3']

        # Label the conditions
        df_new['condition'] = combination
        
        rows.append(df_new)

    test_combined_df = pd.concat(rows, ignore_index=True)


    ## GENERATING Foils Type 1 and Type 2 

    test_cond_corr = test_combined_df[test_combined_df['condition']=='correlated']
    test_cond_iso_l = test_combined_df[test_combined_df['condition']=='isolated-left']
    test_cond_iso_c = test_combined_df[test_combined_df['condition']=='isolated-center']
    test_cond_iso_r = test_combined_df[test_combined_df['condition']=='isolated-right']

    test_cond_corr = test_cond_corr.sample(n=12).reset_index(drop=True)
    test_cond_iso_l = test_cond_iso_l.sample(n=12).reset_index(drop=True)
    test_cond_iso_c = test_cond_iso_c.sample(n=12).reset_index(drop=True)
    test_cond_iso_r = test_cond_iso_r.sample(n=12).reset_index(drop=True)

    test_df = pd.concat([test_cond_corr, test_cond_iso_l,test_cond_iso_c,test_cond_iso_r], axis=0).reset_index(drop=True)

    # foil_categories
    # Define the item categories
    foil_category_1 = ['transposition']*6
    foil_category_2 = ['itemchange']*6

    foil_categories = foil_category_1 + foil_category_2 + foil_category_1 + foil_category_2 +foil_category_1 + foil_category_2 + foil_category_1 + foil_category_2
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
    iso_left_df = test_df[test_df['condition']=='isolated-left']
    iso_center_df = test_df[test_df['condition']=='isolated-center']
    iso_right_df = test_df[test_df['condition']=='isolated-right']

    for conditional_df in [corr_df,iso_left_df,iso_center_df,iso_right_df]:

        size = conditional_df.shape[0]//2
        lefts = ['left'] * size
        rights = ['right'] * size
        target_loc = np.array(lefts+rights)
        np.random.shuffle(target_loc)
        conditional_df['target_loc'] = target_loc
      

    final_test_df = pd.concat([corr_df,iso_left_df,iso_center_df,iso_right_df],axis=0)

    audio_sequences = []
    for row in final_test_df[['item1','casemarker1','item2','casemarker2','item3','casemarker3']].iterrows():
        seq = [word+'.wav' for word in row[1].to_list()]
        audio_sequences.append(seq)
        
        
    final_test_df['target_audio_sequence'] = audio_sequences
    # try:
    #     final_test_df['foil_audio_sequence'] = final_test_df['foil'].apply(lambda x: [w+'.wav' for w in x])
    # except:
    #     final_test_df['foil_audio_sequence'] = final_test_df['foil'].apply(lambda x: [w+'.wav' for w in eval(x)])

    # image sequence 
    image_sequence = []
    for row in final_test_df[['item1','item2','item3']].iterrows():
        seq = [image_association[word] for word in row[1].to_list()]
        image_sequence.append(seq)

    final_test_df['target_image_sequence'] = image_sequence

    try:
        final_test_df['foil_image_sequence'] = final_test_df['foil'].apply(lambda x: [image_association[w] for w in x])
    except:
        final_test_df['foil_image_sequence'] = final_test_df['foil'].apply(lambda x: [image_association[w] for w in eval(x)])
        

    image_sequence = []
    for row in final_test_df[['item1','item2','item3']].iterrows():
        seq = [image_association[word] for word in row[1].to_list()]
        image_sequence.append(seq)

    final_test_df['target_image_sequence'] = image_sequence
    

    print('Saving test-csv new')
    final_test_df.to_csv('./Data/test_v5.csv',index=False)
    print("Invididualising by condition")
    print("Saving files")
    for condition in final_test_df['condition'].unique():
        print(f"- {condition}")
        final_test_df[final_test_df['condition']==condition].to_csv(f'./Data/{condition}_test.csv',index=False)




if __name__ == '__main__':
    # Define the pool of syllabus items
    syllabus_pool = ["barget", "bimdah", "chelad", "dingep", "fisslin", "goorshell",
                    "haagle", "jeelow", "limeber", "makkot", "nellby", "pakrid",
                    "rakken", "sumbark"]

    # Randomly select 10 items from the pool
    selected_items = random.sample(syllabus_pool, 10)

    images = os.listdir('./Images')
    # .DS_Store
    try:
        images.remove('.DS_Store')
    except:
        pass

    image_association = {}
    for image, item in zip(images, selected_items):
        image_association[item] = image
        


    # Generate all possible permutations of the selected items
    all_permutations = list(permutations(selected_items, 3))

    # Filter out invalid permutations (those with repeated items)
    valid_permutations = [p for p in all_permutations if len(set(p)) == len(p)]


    selected_permutations, remaining_items = generate_training_conditions(valid_permutations, image_association)
    print("--"*25)
    generate_test_conditions(valid_permutations, selected_permutations, remaining_items, image_association)


print('-'*25)
print('Job Completed!')




    