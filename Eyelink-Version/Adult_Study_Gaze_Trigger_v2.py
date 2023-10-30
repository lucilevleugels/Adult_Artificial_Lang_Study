import pylink
from psychopy import visual, core, sound, event, gui, data, monitors
import pandas as pd 
import datetime
import os 
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy
from math import hypot


#BLOCK DICTIONARY
BLOCK_DATA_TEST = []
BLOCK_DATA_TRAIN = []

def training_block(win, training_phase_text, train_trial_df, choice_data, iteration):
    
    temp_train_block_data = []
    
    training_phase_text.draw()
    win.flip()
    
    control = event.waitKeys(keyList=['space'])
    if control[0] == 'space':
        
        
        for i, row in enumerate(train_trial_df.iterrows(),1):
            
            block_data = {}
            block_data['block'] = iteration + 1 
            block_data['trial'] = i
            
            
            trial_data = row[1]
            
            audio_items = eval(trial_data['audio_sequence'])
            images = eval(trial_data['image_sequence'])
                
            audio_paths = [os.path.join("./Audio", item) for item in audio_items]
            #sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]

            block_data['audio'] = audio_items
    
            
           
            for j, image in enumerate(images,1):
                block_data[f"S{j}"] = image
                
            
            num_images = len(images)
            spacing = 150  # Adjust the spacing between images as needed
            total_width = (num_images - 1) * spacing
            start_x = -total_width / 2
            
            # Create a list of ImageStim objects with appropriate positions
            image_stims = []
            
            for image_name, i in zip(images, range(num_images)):
                image_path = os.path.join('Images', image_name.strip())
                x = start_x + i * spacing
                image_stim = visual.ImageStim(win, image=image_path, pos=(x, 0), size=(90, 91))
                image_stims.append(image_stim)
            
            
            # Presenting Images & sound
            tk.sendMessage(f'Image Stimulus Presentation Start')
            for image_stim in image_stims:
                image_stim.draw()
            tk.sendMessage(f'Image Stimulus Presentation End')
                
            win.flip()
            
            tk.sendMessage(f'!V TRIAL_VAR Audio-Train {audio_items}')
            
            # for testing 
            for audio in audio_items:
                tk.sendMessage(f'Sound {audio} On_set')
            
#            for sound_stim,audio in zip(sound_stims,audio_items):
#                tk.sendMessage(f'Sound {audio} On_set')
#                sound_stim.play()
#                core.wait(0.6)
            tk.sendMessage(f'Sound stimulus presentation  -- End')
                
           
            
            keys = event.waitKeys(keyList=['space']) 
            temp_train_block_data.append(block_data)
    
    
    return temp_train_block_data.append
    
    
    
            
            
def testing_block(win, testing_phase_test, test_trial_df, choice_data, iteration ):
    
    temp_test_block_data = []
    
    
    testing_phase_text.draw()
    win.flip()
      
    control = event.waitKeys(keyList=['space'])

    if control[0] == 'space':
        
        for i,row in enumerate(test_trial_df.iterrows(),1):
            block_data = {}
            
            block_data['block'] = iteration + 1 
            block_data['trial'] = i
            
            trial_data = row[1]
            #print(trial_data)
            
            audio_items = eval(trial_data['target_audio_sequence'])
            audio_paths = [os.path.join("./Audio", item) for item in audio_items]
            #sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]
            
            block_data['audio'] = audio_items
            
            
            
            target_images = eval(trial_data['target_image_sequence'])
            foil_images = eval(trial_data['foil_image_sequence'])
            
            block_data['Target_image'] = target_images
            block_data['Foil_image'] = foil_images
        
            #block_data['Target_audio_cond1'] = trial_data['Target_audio_cond1']
            #block_data['Target_audio_cond2 '] = trial_data['Target_audio_cond2']
            
            
            target_location = trial_data['target_loc']
            if target_location == 'left':
                foil_location = 'right' 
            else:
                foil_location = 'left'
                
            block_data['Target_Location'] = target_location

            
            # Create image stimuli for target and foil images
            if target_location == 'left':
                target_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(90, 91)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(90, 91)) for img in foil_images]
            else:
                target_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(90, 91)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(90, 91)) for img in foil_images]
                
                target_stimuli, foil_stimuli = foil_stimuli, target_stimuli
                


            # Calculate the positions for target and foil stimuli
            y_position = 0  # Adjust as needed

            # Set horizontal positions for target stimuli on the left
            x_offset_target = -400  # Adjust as needed
            spacing_target = 100  # Adjust the horizontal spacing as needed
            for i, target in enumerate(target_stimuli):
                target_x = x_offset_target + (i * spacing_target)
                target.pos = (target_x, y_position)

            # Set horizontal positions for foil stimuli on the right
            x_offset_foil = 200  # Adjust as needed
            spacing_foil = 100  # Adjust the horizontal spacing as needed
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
                
            tk.sendMessage(f'Image Stimulus Presentation -- End')
            
            # Update the window to show the stimuli
            win.flip()
            
            tk.sendMessage(f'!V TRIAL_VAR Audio-Train {audio_items}')
            # for testing 
            for audio in audio_items:
                tk.sendMessage(f'Sound {audio} On_set')
#            for sound_stim, audio in zip(sound_stim,audio_items):
#                tk.sendMessage(f'Sound {audio} On_set')
#                sound_stim.play()
#                core.wait(0.8)
            tk.sendMessage(f'Sound stimulus presentation  -- End')
            
            start_time = core.getTime()
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            elapsed_time = core.getTime() - start_time
            block_data['Response Time'] = elapsed_time

            
            tk.sendMessage(f'!V TRIAL_VAR Response-Time {elapsed_time}')
            

            answer = 'left' if 'left' in keys else 'right'
            block_data['Answer'] = answer
            block_data['Accuracy'] = 1 if answer == target_location else 0
            tk.sendMessage(f'!V TRIAL_VAR Keypress {answer}')
            

            
            if 'escape' in keys:
                break
                
            temp_test_block_data.append(block_data)
            
    return temp_test_block_data


# CONDITION 

# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["correlated","isolated-left","isolated-center","isolated-right"])
choice_data = choice_dialog.show()


# TRIAL CSV's

train_df = pd.read_csv('Trial_Info/train_v3.csv')
test_df = pd.read_csv('Trial_Info/test_v3.csv')


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
# Screen resolution
SCN_W, SCN_H = (2280, 1580)
# Open a PsyhocPy window
win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', color='white')


# INFORMATION 
training_phase_text = visual.TextStim(win, text="Training Phase", height=50, color='black', pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=50, color='black',  pos=(0,0))



# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
coords = f"screen_pixel_coords = 0 0 {SCN_W - 1} {SCN_H - 1}"
tk.sendCommand(coords)
# Request Pylink to use the custom EyeLinkCoreGraphicsPsychoPy library
# to draw calibration graphics (target, camera image, etc.)
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
genv.setCalibrationSounds('off','off', 'off')

pylink.openGraphicsEx(genv)

# Calibrate the tracker
calib_msg = visual.TextStim(win, text='Press ENTER twice to calibrate',height=50, color='black') 
calib_msg.draw()
win.flip()
tk.doTrackerSetup()


# Run 3 trials in a for-loop
# in each trial, first show a fixation dot, wait for the participant # to gaze at the fixation dot, then present an image for 2 secs
for i in range(2):

    
     # Shuffle
    train_trial_df = train_dfs[choice_data[0]].sample(frac=1)
    test_trial_df = test_dfs[choice_data[0]].sample(frac=1)

    
   
   # Prepare the fixation dot in memory
    fix = visual.GratingStim(win, tex='None', mask='circle', size=50, pos=(0,400), color='black')



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
    
   
   

    tk.sendMessage(f'!V TRIAL_VAR Train-Block {i}')
    tk.sendMessage(f'Train-Block {i}')
    train_block_data = training_block(win, training_phase_text, train_trial_df, choice_data, i)
    # can introduce some kind of delay here in between
    tk.sendMessage(f'!V TRIAL_VAR Test-Block {i}')
    tk.sendMessage(f'Test-Block {i}')
    test_block_data  = testing_block(win, testing_phase_text, test_trial_df, choice_data, i)
    
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
print(BLOCK_DATA_TRAIN)
print("-")
print(BLOCK_DATA_TEST)
train_block_df = pd.DataFrame(BLOCK_DATA_TRAIN).fillna('-')
train_block_df.to_csv('SOURCE-CSV_3.csv')

test_block_df = pd.DataFrame(BLOCK_DATA_TEST)
test_block_df.to_csv('Test_3.csv')


# Download the EDF data file from Host
#timestring = datetime.datetime.now().strftime("%H:%M:%S_%d_%b_%Y")
tk.receiveDataFile('psychopy.edf', f'Adult_study_3.edf')
# Close the link to the tracker
tk.close()
# Close the graphics
win.close()
core.quit()

            
        
