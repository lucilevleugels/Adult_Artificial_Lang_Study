import pylink
from psychopy import visual, core, sound, event, gui, data, monitors
import pandas as pd 
import datetime
import os 
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from math import hypot

mon = monitors.Monitor('testMonitor')


#BLOCK DICTIONARY
BLOCK_DATA_TEST = []
BLOCK_DATA_TRAIN = []

# PATHS 
DATA_TRAIN_PATH = "../Data"
DATA_TEST_PATH = "../Data"

AUDIO_PATH = "../Audio"
IMAGE_PATH = "../Images"
PROGESS_IMAGE_PATH = "../progress_bar_images"

RESULTS = "./Results"

# PARAMETERS 
AUDIO_DELAY = 0.9

# TEST FLAG
TEST_FLAG = False  
TEST_TRIALS = 6

# BLOCKS
BLOCKS = range(1,5)

# IMAGE PARAMS
IMAGE_DIMS = (350 , 351)

# FOR DELL 27 INCH
# Screen resolution
SCN_W, SCN_H = (3825,2010)


def create_repetitions(repetition, df):
    
    row_copy = df.iloc[repetition-1,:]
    row_copy = pd.DataFrame(row_copy).T

    before_r = df.iloc[:repetition, :]
    after_r = df.iloc[repetition:, :]
        
    return pd.concat([before_r, row_copy, after_r],axis=0)

def training_block(tk, win, training_phase_text, space_bar, train_block, choice_data, iteration):
    
    
    
    # REPETITION PARAMS
    repetition_params = {1: (3,11,16), 2:(6,15,19), 3:(2,10,18), 4:(9,14,20)}
    
    good_job = visual.TextStim(win, text="Good Job, you found the repetition!", height=70, color=(-1, -1, -1), pos=(0,0))
    bad_job = visual.TextStim(win, text="Please Play Attention, you missed the repetition.", height=70, color=(-1, -1, -1), pos=(0,0))
    
    temp_train_block_data = []
    
    training_phase_text.draw()
    win.flip()
    core.wait(1)
    
    space_bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])
    
    if control[0] == 'space':
        
        global TEST_FLAG
        
        # FOR TESTING THE SCRIPT 
        if TEST_FLAG:
            train_block = train_block.iloc[:TEST_TRIALS,:]
        else:
            train_block = train_block
        
        
        # to identify the repetition
        hashmap={}
        for i, row in enumerate(train_block.iterrows(),1):
            
            
            
            tk.sendMessage(f'TRIALID {i}')
            tk.sendMessage(f"TRAINING BLOCK {iteration} ")
            tk.sendMessage(f'!V TRIAL_VAR Train-Block {iteration}')
            
            trial_data = row[1]
            
            # increment for repetition
            hashmap[trial_data['trial']] = hashmap.get(trial_data['trial'],0)+1
            
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
            spacing = 350  # Adjust the spacing between images as needed
            total_width = (num_images - 1) * spacing
            start_x = -total_width / 2
            
            # Create a list of ImageStim objects with appropriate positions
            image_stims = []
            
            for image_name, i in zip(images, range(num_images)):
                image_path = os.path.join(IMAGE_PATH, image_name.strip())
                x = start_x + i * spacing
                image_stim = visual.ImageStim(win, image=image_path, pos=(x, 0), size=IMAGE_DIMS)
                image_stims.append(image_stim)
            
            
            # Presenting Images & sound
            tk.sendMessage(f'Image Stimulus Presentation Start')
            for image_stim in image_stims:
                image_stim.draw()
            win.flip()
            
            
                
            
            tk.sendMessage(f'!V TRIAL_VAR Audio-Train {audio_items}')
            
                
            
            for sound_stim,audio in zip(sound_stims,audio_items):
                tk.sendMessage(f'Sound {audio} On_set')
                sound_stim.play()
                core.wait(AUDIO_DELAY)
            tk.sendMessage(f'Sound stimulus presentation  -- End')
                
           
        
            # space bar screen
            space_bar.draw()
            win.flip()
            keys = event.waitKeys(keyList=['space', 'down','escape'])
           
            if keys[0] == 'down' and hashmap[trial_data['trial']] == 2:
                
                block_data['repetition_found'] = 1
                tk.sendMessage(f'!V TRIAL_VAR Repetition-Found 1')
               
                good_job.draw()
                
                win.flip()
                core.wait(2)
                space_bar.draw()
                win.flip()
                keys = event.waitKeys(keyList=['space', 'escape'])
                if keys[0] == 'escape':
                    
                    # Stop recording
                    tk.stopRecording()

                    # Close the EDF data file on the Host
                    tk.closeDataFile()
                    
                    tk.receiveDataFile('psychopy.edf', f'partial.edf')
                    # Close the link to the tracker
                    tk.close()
                    ## Close the graphics
                    win.close()
                    core.quit()
            
            elif hashmap[trial_data['trial']] == 2:
                bad_job.draw()
                win.flip()
                core.wait(2)
                tk.sendMessage(f'!V TRIAL_VAR Repetition-Found 0')
                block_data['repetition_found'] = 0
                
                space_bar.draw()
                win.flip()
                keys = event.waitKeys(keyList=['space', 'escape'])
                
                if keys[0] == "escape":
                    # Stop recording
                    tk.stopRecording()

                    # Close the EDF data file on the Host
                    tk.closeDataFile()
                    
                    tk.receiveDataFile('psychopy.edf', f'partial.edf')
                    # Close the link to the tracker
                    tk.close()
                    ## Close the graphics
                    win.close()
                    core.quit()
               
            elif keys[0] == 'escape':
                    
                    # Stop recording
                    tk.stopRecording()

                    # Close the EDF data file on the Host
                    tk.closeDataFile()
                    
                    tk.receiveDataFile('psychopy.edf', f'partial.edf')
                    # Close the link to the tracker
                    tk.close()
                    ## Close the graphics
                    win.close()
                    core.quit()
               
            
            tk.sendMessage(f'Image Stimulus Presentation End')
            
            temp_train_block_data.append(block_data)
            
            #tk.sendMessage('TRIAL_RESULT 0')
            tk.sendMessage(f"TRAINING BLOCK {iteration} END ")
            
    
    
    return temp_train_block_data
    
    

            
def testing_block(tk, win, testing_phase_text, space_bar, test_trial_df, choice_data, iteration ):
    
    
    
    temp_test_block_data = []
    
    
    testing_phase_text.draw()
    win.flip()
    core.wait(1)
    
    space_bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])

    if control[0] == 'space':
        
        # FOR TESTING THE SCRIPT 
        if TEST_FLAG:
            test_trial_df = test_trial_df.iloc[:TEST_TRIALS,:]
        else:
            test_trial_df = test_trial_df
        
        for i,row in enumerate(test_trial_df.iterrows(),1):
            
            tk.sendMessage(f'TRIALID {i}')
            tk.sendMessage(f'!V TRIAL_VAR Test-Block {iteration}')
            
            block_data = {}
            
            
            trial_data = row[1]
            block_data['block'] = iteration
            block_data['trial'] = trial_data['trial']
            
           

            
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
                target_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=IMAGE_DIMS) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=IMAGE_DIMS) for img in foil_images]
            else:
                target_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=IMAGE_DIMS) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join(IMAGE_PATH,img.strip()), size=IMAGE_DIMS) for img in foil_images]
                
                target_stimuli, foil_stimuli = foil_stimuli, target_stimuli
                
            

            # Calculate the positions for target and foil stimuli
            y_position = 0  # Adjust as needed

            # Set horizontal positions for target stimuli on the left
            x_offset_target = -1300  # Adjust as needed
            spacing_target = 350  # Adjust the horizontal spacing as needed
            for i, target in enumerate(target_stimuli):
                target_x = x_offset_target + (i * spacing_target)
                target.pos = (target_x, y_position)

            # Set horizontal positions for foil stimuli on the right
            x_offset_foil = 700  # Adjust as needed
            spacing_foil = 350  # Adjust the horizontal spacing as needed
            for i, foil in enumerate(foil_stimuli):
                foil_x = x_offset_foil + (i * spacing_foil)
                foil.pos = (foil_x, y_position)

            # Display all target stimuli and foil stimuli
            tk.sendMessage(f'Image Stimulus Presentation -- Target, Position {target_location}')
            for target in target_stimuli:
                target.draw()
            tk.sendMessage(f'Image Stimulus Presentation -- Foil')
            for foil in foil_stimuli:
                foil.draw()
                
            
            
            # Update the window to show the stimuli
            win.flip()
            tk.sendMessage(f'Sound stimulus presentation Start')
            tk.sendMessage(f'!V TRIAL_VAR Audio-Train {audio_items}')
           
            for sound_stim, audio in zip(sound_stims, audio_items):
                tk.sendMessage(f'Sound {audio} On_set')
                sound_stim.play()
                core.wait(AUDIO_DELAY)
            tk.sendMessage(f'Sound stimulus presentation End')
            
            start_time = core.getTime()
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            elapsed_time = core.getTime() - start_time
            block_data['Response Time'] = elapsed_time
            tk.sendMessage(f'Image Stimulus Presentation -- End')
            
            tk.sendMessage(f'!V TRIAL_VAR Response-Time {elapsed_time}')
            

            answer = 'left' if 'left' in keys else 'right'
            block_data['Answer'] = answer
            block_data['Accuracy'] = 1 if answer == target_location else 0
            tk.sendMessage(f'!V TRIAL_VAR Keypress {answer}')
            
            
            if 'escape' in keys:
                break
                
            space_bar.draw()
            win.flip()
            control = event.waitKeys(keyList=['space'])
                
            temp_test_block_data.append(block_data)
            
            #tk.sendMessage('TRIAL_RESULT 0')
            
    return temp_test_block_data


# FILE NAME
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

# CONDITION 
# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["correlated","isolated-left","isolated-center","isolated-right"])
choice_data = choice_dialog.show()


# TRIAL CSV's
train_df = pd.read_csv(os.path.join(DATA_TRAIN_PATH, "train_v5_lv.csv"))
test_df = pd.read_csv(os.path.join(DATA_TEST_PATH, "test_v5_lv.csv"))


# df by condition
train_dfs = {}
for condition in train_df['condition'].unique():
        train_dfs[condition] = train_df[train_df['condition']==condition]
        
test_dfs = {}
for condition in test_df['condition'].unique():
        test_dfs[condition] = test_df[test_df['condition']==condition]


# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')
# Open an EDF data file on the Host PC
tk.openDataFile('psychopy.edf')
# Put the tracker in offline mode before we change tracking parameters
tk.setOfflineMode()
# Make all types of eye events available over the link, especially the
# FIXUPDATE event, which reports the current status of a fixation at
# predefined intervals (default = 50 ms)
event_flags = 'LEFT,RIGHT,FIXATION,FIXUPDATE,SACCADE,BLINK,BUTTON,INPUT'
tk.sendCommand(f'link_event_filter = {event_flags}')

# Open a PsyhocPy window
#win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', color='white')
#win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', color='white')
win = visual.Window(fullscr=True, units='pix', color='white')
(SCN_W, SCN_H) = win.size
#win = visual.Window((3900,2050), fullscr=False, units='pix', color='white')

#win = visual.Window(fullscr=True, units='pix', color='white')

# INFORMATION 
space_bar_text = '''Press Spacebar to Continue'''

training_phase_text = visual.TextStim(win, text="Training Phase", height=70, color=(-1, -1, -1), pos=(0,0))

space_bar = visual.TextStim(win, text=space_bar_text, height=70, color='black', pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=70 , color=(-1, -1, -1), pos=(0,0))



# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
coords = f"screen_pixel_coords = 0 0 {SCN_W - 1} {SCN_H - 1}"
tk.sendCommand(coords)
tk.sendCommand("calibration_type = HV9")
# Request Pylink to use the custom EyeLinkCoreGraphicsPsychoPy library
# to draw calibration graphics (target, camera image, etc.)
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
genv.setCalibrationSounds('off','off', 'off')

pylink.openGraphicsEx(genv)

# Calibrate the tracker
calib_msg = visual.TextStim(win, text='Press calibrate for calibration',height=50, color='black') 
calib_msg.draw()
win.flip()
tk.doTrackerSetup()



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

repetition_params = {1: (3,11,16), 2:(6,15,19), 3:(2,10,18), 4:(9,14,20)}


# in each trial, first show a fixation dot, wait for the participant # to gaze at the fixation dot, then present an image for 2 secs
for iteration in BLOCKS:
    
    
    print(f"BLOCK {iteration}")
    
    train_block = train_trial_df[train_trial_df['block_index'] == iteration]
    test_block = test_trial_df[test_trial_df['Block'] == iteration]
    repetitions = repetition_params[iteration]
   
    for i, repetition in enumerate(repetitions, 0):
        train_block = create_repetitions(repetition+i, train_block.reset_index(drop=True))
   
   # Prepare the fixation dot in memory
    fix = visual.GratingStim(win, tex='None', mask='circle', size=50, pos=(0,400), color='black')

    
    # PROGRESS BAR 
    bar = visual.ImageStim(win, image=os.path.join(PROGESS_IMAGE_PATH, f"progressbar{iteration}.png"),pos=(0,0), size=(2200,1250))

    # Put tracker in Offline mode before we start recording
    tk.setOfflineMode()
    # Start recording
    tk.startRecording(1, 1, 1, 1)
    # Wait for the block start event to arrive, give a warning # if no event or sample is available
    block_start = tk.waitForBlockStart(100, 1, 1)
    if block_start == 0:
            print("ERROR: No link data received!")
    # Check eye availability; 0-left, 1-right, 2-binocular
    # read data from the right eye if tracking in binocular mode 
    eye_to_read = tk.eyeAvailable()
    if eye_to_read == 2:
        eye_to_read = 1
    
    # Show the fixation dot
    fix.draw()
    win.flip()
    
    # Gaze trigger
    # wait for gaze on the fixation dot (for a minimum of 300 ms) 
    fix_dot_x, fix_dot_y = (SCN_W/2.0, SCN_H/2.0)
    triggered = False
    fixation_start_time = -32768
    
    while not triggered:
        # Check if any new events are available 
        dt = tk.getNextData()
        if dt == pylink.FIXUPDATE:
            ev = tk.getFloatData()
            if ev.getEye() == eye_to_read:
                # 1 deg = ? pixels in the current fixation
                ppd_x, ppd_y = ev.getEndPPD()
        
                # Get the gaze error
                gaze_x, gaze_y = ev.getAverageGaze() 
                gaze_error = hypot((gaze_x - fix_dot_x)/ppd_x,
                                                   (gaze_y - fix_dot_y)/ppd_y)
                if gaze_error < 5:
                    # Update fixation_start_time, following the first 
                    # FIXUPDATE event
                    if fixation_start_time < 0:
                        fixation_start_time = ev.getStartTime()
                    else:
                    # Break if the gaze is on the fixation dot
                    # for > 300 ms
                        if (ev.getEndTime() - fixation_start_time) >= 5:
                            triggered = True 
                else:
                    fixation_start_time = -32768
    
   
   

   
    #tk.sendMessage(f'Train-Block {iteration}')
    tk.sendMessage(f'!V TRIAL_VAR Train-Block {iteration}_GazeTrigger')
    train_block_data = training_block(tk, win, training_phase_text, space_bar, train_block, choice_data, iteration)
    # can introduce some kind of delay here in between
    #tk.sendMessage(f'Train-Block {iteration} End')
    
   
    #tk.sendMessage(f'Test-Block {iteration}')
    tk.sendMessage(f'!V TRIAL_VAR Test-Block {iteration}_GazeTrigger')
    test_block_data  = testing_block(tk, win, testing_phase_text, space_bar, test_block, choice_data, iteration)
    
    
    #tk.sendMessage(f'Test-Block {iteration} End')
    
    bar.draw()
    win.flip()
    control = event.waitKeys(keyList=['space'])
    
    BLOCK_DATA_TRAIN.append(train_block_data)
    BLOCK_DATA_TEST.append(test_block_data)
    

    
    # Clear the screen
    win.flip()
    core.wait(0.5)
    
    
    
# Stop recording
tk.stopRecording()

# Close the EDF data file on the Host
tk.closeDataFile()

    
# SAVING BLOCK DATA
dfs = []
for block in BLOCK_DATA_TRAIN:
    dfs.append(pd.DataFrame(block))
    
train_block_df = pd.concat(dfs,axis=0).fillna('-')
train_block_df.to_csv(f'Train-Block-Source_{choice_data[0]}_{file_name}.csv') 

dfs = []
for block in BLOCK_DATA_TEST:
    dfs.append(pd.DataFrame(block))

test_block_df = pd.concat(dfs,axis=0)
test_block_df.to_csv(f'Test-Block-Source_{choice_data[0]}_{file_name}.csv')


# Download the EDF data file from Host
#timestring = datetime.datetime.now().strftime("%H:%M:%S_%d_%b_%Y")
tk.receiveDataFile('psychopy.edf', f'{file_name}.edf')
# Close the link to the tracker
tk.close()
## Close the graphics
win.close()
core.quit()

            
        
