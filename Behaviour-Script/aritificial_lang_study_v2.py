from psychopy import visual, core, sound, event, gui, data
import os, csv
import pandas as pd 
import datetime
import warnings
warnings.filterwarnings('ignore')

# PATHS 
DATA_TRAIN_PATH = "../Data"
DATA_TEST_PATH = "../Data"

AUDIO_PATH = "../Audio"
IMAGE_PATH = "../Images"
PROGESS_IMAGE_PATH = "../progress_bar_images"

RESULTS = "./Results"

# TEST FLAG
TEST_FLAG = True  
TEST_TRIALS = 1

# PARAMETERS
AUDIO_DELAY = 0.9

# REPETITION PARAMS
repetition_params = {1: (3,11,16), 2:(6,15,19), 3:(2,10,18), 4:(9,14,20)}


def create_repetitions(repetition, df):
    
    row_copy = df.iloc[repetition-1,:]
    row_copy = pd.DataFrame(row_copy).T

    before_r = df.iloc[:repetition, :]
    after_r = df.iloc[repetition:, :]
        
    return pd.concat([before_r, row_copy, after_r],axis=0)


file_name = '100'

# Prompt user to specify an EDF data filename
# before we open a fullscreen window
dlg_title = 'Enter Participant Data File Name'
dlg_prompt = 'Please enter a file name with 8 or fewer characters\n'
             

# loop until we get a valid filename

dlg = gui.Dlg(dlg_title)
dlg.addText(dlg_prompt)
dlg.addField('Participant ID:', file_name)
# show dialog and wait for OK or Cancel
ok_data = dlg.show()
if dlg.OK:  # if ok_data is not None
    print('Participant data filename: {}'.format(ok_data[0]))
else:
    print('user cancelled')
    core.quit()
    sys.exit()

# get the string entered by the experimenter
file_name = dlg.data[0]


os.makedirs(os.path.join(RESULTS, f"{file_name}"), exist_ok=True)


# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["correlated","isolated-left","isolated-center","isolated-right"])
choice_data = choice_dialog.show()





#SCN_W, SCN_H = (1280, 800)
# Open a PsyhocPy window with the "allowStencil" option 
win = visual.Window(fullscr=True, units='pix', allowStencil=True, color=(1,1,1))


train_df = pd.read_csv(os.path.join(DATA_TRAIN_PATH, "train_v4.csv"))
test_df = pd.read_csv(os.path.join(DATA_TEST_PATH, "test_v4.csv"))



# df by condition
train_dfs = {}
for condition in train_df['condition'].unique():
        train_dfs[condition] = train_df[train_df['condition']==condition]
        
test_dfs = {}
for condition in test_df['condition'].unique():
        test_dfs[condition] = test_df[test_df['condition']==condition]



space_bar_text = '''PRESS SPACE-BAR TO CONTINUE'''

training_phase_text = visual.TextStim(win, text="Training Phase", height=70, color=(-1, -1, -1), pos=(0,0))
good_job = visual.TextStim(win, text="Good Job, you found the repetition!", height=70, color=(-1, -1, -1), pos=(0,0))
bad_job = visual.TextStim(win, text="Please pay attention, you missed the repetition", height=70, color=(-1, -1, -1), pos=(0,0))
space_bar = visual.TextStim(win, text=space_bar_text, height=70, color='black', pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=70 , color=(-1, -1, -1), pos=(0,0))

#BLOCK DICTIONARY
BLOCK_DATA_TRAIN = []
BLOCK_DATA_TEST = []


# selecting train set based on the condition 
train_trial_df = train_dfs[choice_data[0]]
test_trial_df = test_dfs[choice_data[0]]

# adding block index
ones = [1]*20
twos = [2]*20
threes = [3]*20
fours = [4]*20

block_index = ones + twos + threes + fours
train_trial_df['block_index'] = block_index

for iteration in range(1,3):
    
    bar = visual.ImageStim(win, image=os.path.join(PROGESS_IMAGE_PATH, f"progressbar{iteration}.jpg"),pos=(0,0), size=(1500,1250))
    
    print(f"BLOCK {iteration}")
    
    train_block = train_trial_df[train_trial_df['block_index'] == iteration]
    repetitions = repetition_params[iteration]
   
    for i, repetition in enumerate(repetitions, 0):
        train_block = create_repetitions(repetition+i, train_block.reset_index(drop=True))
        
    
    training_phase_text.draw()
    win.flip()
    core.wait(1)
    
    space_bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])
    if control[0] == 'space':
        
        # FOR TESTING THE SCRIPT 
        if TEST_FLAG:
            train_block = train_block.iloc[:TEST_TRIALS,:]
        else:
            train_block = train_block
        
        for i, row in enumerate(train_block.iterrows(),1):
            
            trial_data = row[1]
            
            block_data = {}
            block_data['block'] = iteration
            block_data['trial'] = trial_data['trial']
            
            audio_items = eval(trial_data['audio_sequence'])
            images = eval(trial_data['image_sequence'])
                
            audio_paths = [os.path.join(AUDIO_PATH, item) for item in audio_items]
            sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]

            block_data['audio'] = audio_items
    
            
           
            for j, image in enumerate(images,1):
                block_data[f"S{j}"] = image
                
            
            num_images = len(images)
            spacing = 300  # Adjust the spacing between images as needed
            total_width = (num_images - 1) * spacing
            start_x = -total_width / 2
            
            # Create a list of ImageStim objects with appropriate positions
            image_stims = []
            
            for image_name, i in zip(images, range(num_images)):
                image_path = os.path.join(IMAGE_PATH, image_name.strip())
                x = start_x + i * spacing
                image_stim = visual.ImageStim(win, image=image_path, pos=(x, 0), size=(350 , 351))
                image_stims.append(image_stim)
            
            
            # Presenting Images & sound
            for image_stim in image_stims:
                image_stim.draw()

                
            win.flip()
            
            for sound_stim in sound_stims:
                sound_stim.play()
                core.wait(AUDIO_DELAY)
                
           
                
            
            space_bar.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'down'])

            if keys[0] == 'down':
                
                block_data['repetition_found'] = 1
                good_job.draw()
                win.flip()
                core.wait(1)
                
            else:
                block_data['repetition_found'] = 0
                bad_job.draw()
                win.flip()
                core.wait(1)
            
            
            BLOCK_DATA_TRAIN.append(block_data)
            

    
    #print(BLOCK_DATA_TRAIN)
        
      
    #TESTING PHASE
    testing_phase_text.draw()
    win.flip()
    core.wait(1)
      
    
    space_bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])
    
    

    if control[0] == 'space':
        
        if TEST_FLAG:
            test_trial_df = test_trial_df.iloc[:TEST_TRIALS,:]
        else:
            test_trial_df = test_trial_df
        
        for i,row in enumerate(test_trial_df.iterrows(),1):
            block_data = {}
            
            trial_data = row[1]
            
            block_data['block'] = iteration
            block_data['trial'] = trial_data['trial']
            
            
            #print(trial_data)
            
            
            
            audio_items = eval(trial_data['target_audio_sequence'])
            audio_paths = [os.path.join(AUDIO_PATH, item) for item in audio_items]
            sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]
            
            block_data['audio'] = audio_items
            
            
            
            target_images = eval(trial_data['target_image_sequence'])
            foil_images = eval(trial_data['foil_image_sequence'])
            
            block_data['Target_image'] = target_images
            block_data['Foil_image'] = foil_images
    
            
            
            target_location = trial_data['target_loc']
            if target_location == 'left':
                foil_location = 'right' 
            else:
                foil_location = 'left'
                
            block_data['Target_Location'] = target_location

            
            # Create image stimuli for target and foil images
            if target_location == 'left':
                target_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=(350 , 351)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=(350 , 351)) for img in foil_images]
            else:
                target_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=(350 , 351)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=(350 , 351)) for img in foil_images]
                
                target_stimuli, foil_stimuli = foil_stimuli, target_stimuli
                


            # Calculate the positions for target and foil stimuli
            y_position = 0  # Adjust as needed

            # Set horizontal positions for target stimuli on the left
            x_offset_target = -1300  # Adjust as needed
            spacing_target = 300  # Adjust the horizontal spacing as needed
            for i, target in enumerate(target_stimuli):
                target_x = x_offset_target + (i * spacing_target)
                target.pos = (target_x, y_position)

            # Set horizontal positions for foil stimuli on the right
            x_offset_foil = 700  # Adjust as needed
            spacing_foil = 300  # Adjust the horizontal spacing as needed
            for i, foil in enumerate(foil_stimuli):
                foil_x = x_offset_foil + (i * spacing_foil)
                foil.pos = (foil_x, y_position)

            # Display all target stimuli and foil stimuli

            for target in target_stimuli:
                target.draw()
            for foil in foil_stimuli:
                foil.draw()
                
            # Update the window to show the stimuli
            win.flip()
            
            for sound_stim in sound_stims:
                sound_stim.play()
                core.wait(AUDIO_DELAY)
            
            
            start_time = core.getTime()
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            elapsed_time = core.getTime() - start_time
            block_data['Response Time'] = elapsed_time

            answer = 'left' if 'left' in keys else 'right'
            block_data['Answer'] = answer
            block_data['Accuracy'] = 1 if answer == target_location else 0
            
            BLOCK_DATA_TEST.append(block_data)

            
            if 'escape' in keys:
                break
                
                
            space_bar.draw()
            win.flip()
            control = event.waitKeys(keyList=['space'])
                
            
           
    bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])
        
                    
train_block_df = pd.DataFrame(BLOCK_DATA_TRAIN).fillna('-')
train_block_df.to_csv(os.path.join(os.path.join(RESULTS, f"{file_name}"),f'Train-Block-Source_{choice_data[0]}.csv'))

test_block_df = pd.DataFrame(BLOCK_DATA_TEST)
test_block_df.to_csv(os.path.join(os.path.join(RESULTS, f"{file_name}"), f'Testing-Data_{choice_data[0]}.csv'))




    