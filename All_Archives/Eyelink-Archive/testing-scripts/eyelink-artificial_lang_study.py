#!/usr/bin/env python3
#
# Filename: gaze_contingent_window.py
# Author: Zhiguo Wang
# Date: 2/6/2021
#
# Description:
# A script that displays a Cookie Monster image at the top center of the screen
# and shows a red pointer at the gaze position using PsychoPy and EyeLink.

import pylink
import os 
from psychopy import visual, core, sound, event, gui, data
import pandas as pd 
from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy


# CONDITION 
# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["Condition 1", "Condition 2"])
choice_data = choice_dialog.show()


# TRIAL CSV's
train_df = pd.read_csv('Trial_Info/Training_Trails_Adult_Lang_Study.csv')
test_df = pd.read_csv('Trial_Info/Testing_Trials_Adult_Lang_Study.csv')


#BLOCK DICTIONARY
BLOCK_DATA_TRAIN = []
BLOCK_DATA_TEST = []


# Connect to the tracker
tk = pylink.EyeLink('100.1.1.1')

# Open an EDF data file
tk.openDataFile('psychopy.edf')

# Put the tracker in offline mode before we change tracking parameters
tk.setOfflineMode()

# Make all types of sample data available over the link
sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,PUPIL,HREF,AREA,STATUS,INPUT'
tk.sendCommand(f'link_sample_data  = {sample_flags}')

SCN_W, SCN_H = (1280, 800)

# Open a Psychopy window with the "allowStencil" option 
win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', allowStencil=True,color=(1,1,1))

# INFORMATION 
training_phase_text = visual.TextStim(win, text="Training Phase", height=50,color='black', pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=50,color='black',  pos=(0,0))

# Pass the display pixel coordinates (left, top, right, bottom) to the tracker
coords = f"screen_pixel_coords = 0 0 {SCN_W - 1} {SCN_H - 1}"
tk.sendCommand(coords)

# Request Pylink to use the custom EyeLinkCoreGraphicsPsychoPy library
# to draw calibration graphics (target, camera image, etc.)
genv = EyeLinkCoreGraphicsPsychoPy(tk, win)
pylink.openGraphicsEx(genv)

# Calibrate the tracker
calib_msg = visual.TextStim(win, text='Press ENTER to calibrate', color='black')
calib_msg.draw()
win.flip()
tk.doTrackerSetup()

# Load the Cookie Monster image
cookie_monster_img = visual.ImageStim(win, image='target.png', size=(200, 200))
cookie_monster_img.pos = (0, SCN_H / 2 - 100)  # Position at the top center

# Create a red pointer stimulus
red_pointer = visual.Circle(win, radius=5, fillColor='red', lineColor='red')

# Create a "Welcome" text stimulus
welcome_text = visual.TextStim(win, text='Starting Trial', pos=(0, -50), height=50,color='black',)


# Define the bounding box around the Cookie Monster image
cookie_monster_bbox = visual.Rect(win, width=200, height=200, pos=cookie_monster_img.pos)

# Put tracker in Offline mode before we start recording
tk.setOfflineMode()

# Start recording
tk.startRecording(1, 1, 1, 1)

# Cache some samples
pylink.msecDelay(100)

# Initialize a variable to track whether the "Welcome" text is displayed
welcome_displayed = False

# Initialize a variable to track whether the gaze is on the Cookie Monster
gaze_on_cookie_monster = False

# Initialize a variable to track the state of the program
program_state = 'running'

# Show the Cookie Monster image at the beginning of the experiment
cookie_monster_img.draw()
win.flip()
core.wait(2)

# Show the red pointer at the gaze coordinates
while program_state == 'running':
    # Check for new samples 
    smp = tk.getNewestSample() 
    if smp is not None:
        if smp.isRightSample():
            gaze_x, gaze_y = smp.getRightEye().getGaze()
        elif smp.isLeftSample():
            gaze_x, gaze_y = smp.getLeftEye().getGaze()
        
        # Calculate PsychoPy coordinates
        psycho_x = gaze_x - SCN_W / 2.0
        psycho_y = SCN_H / 2.0 - gaze_y
        
#        # Draw the red pointer at the gaze position
#        red_pointer.pos = (psycho_x, psycho_y)
#        red_pointer.draw()
        
        # Check if gaze is within the bounding box of the Cookie Monster image
        if cookie_monster_bbox.contains(psycho_x, psycho_y):
            # Display the "Welcome" text and change program state
            if not welcome_displayed:
                welcome_text.draw()
                win.flip()
                core.wait(2)
                welcome_displayed = True
                program_state = 'start'
        else:
            welcome_displayed = False
        
        win.flip()

# Display the sentences based on the program state
if program_state == 'start':
    for iteration in range(1):
    
        # Shuffle
        test_df = test_df.sample(frac=1)
        train_df = train_df.sample(frac=1)
        

        training_phase_text.draw()
        win.flip()
        control = event.waitKeys(keyList=['space'])

        if control[0] == 'space':
            
            
            for i,row in enumerate(train_df.iterrows(),1):
                block_data = {}
                block_data['block'] = iteration + 1 
                block_data['trial'] = i
                
                
                trial_data = row[1]
                if choice_data[0] == "Condition 1":
                    CONDITION = 1 
                    condition_column = "Condition 1"
                else:
                    CONDITION = 2
                    condition_column = "Condition 2"
                audio_path = os.path.join('Audio',trial_data[condition_column] + '.wav')
                
                block_data['audio'] = audio_path[:-4]
        
                sound_stim = sound.Sound(audio_path)
                images = trial_data['Visual'].split(',')
                
                for j, image in enumerate(images,1):
                    block_data[f"S{j}"] = image
                    
                
                num_images = len(images)
                spacing = 70  # Adjust the spacing between images as needed
                total_width = (num_images - 1) * spacing
                start_x = -total_width / 2
                
                # Create a list of ImageStim objects with appropriate positions
                image_stims = []
                
                for image_name, i in zip(images, range(num_images)):
                    image_path = os.path.join('Images', image_name.strip())
                    x = start_x + i * spacing
                    image_stim = visual.ImageStim(win, image=image_path, pos=(x, 0), size=(61, 61))
                    image_stims.append(image_stim)
                
                
                # Presenting Images
                sound_stim.play()
                for image_stim in image_stims:
                    image_stim.draw()
                    
                win.flip()
                    
                
                BLOCK_DATA_TRAIN.append(block_data)
                keys = event.waitKeys(keyList=['space']) 
                
        
    #TESTING PHASE
    testing_phase_text.draw()
    win.flip()
      
    control = event.waitKeys(keyList=['space'])

    if control[0] == 'space':
        
        for i,row in enumerate(test_df.iterrows(),1):
            block_data = {}
            
            block_data['block'] = iteration + 1 
            block_data['trial'] = i
            
            trial_data = row[1]
            #print(trial_data)
            
            if CONDITION == 1:
                condition_column = f"Target_audio_cond{CONDITION}"
                audio_path = os.path.join('Audio',trial_data[condition_column] + '.wav')
            else:
                condition_column = f"Target_audio_cond{CONDITION}"
                audio_path = os.path.join('Audio',trial_data[condition_column] + '.wav')
            
            sound_stim = sound.Sound(audio_path)
            
            target_images = trial_data['Target_image'].split(',')
            foil_images = trial_data['Foil_image'].split(',')
            
            block_data['Target_image'] = target_images
            block_data['Foil_image'] = foil_images
        
            block_data['Target_audio_cond1'] = trial_data['Target_audio_cond1']
            block_data['Target_audio_cond2 '] = trial_data['Target_audio_cond2']
            
            
            target_location = trial_data['Target_Location']
            if target_location == 'left':
                foil_location = 'right' 
            else:
                foil_location = 'left'
                
            block_data['Target_Location'] = target_location


            # Create image stimuli for target and foil images
            if target_location == 'left':
                target_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(61, 61)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(61, 61)) for img in foil_images]
            else:
                target_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(61, 61)) for img in target_images]
                foil_stimuli = [visual.ImageStim(win, image=os.path.join('Images',img.strip()), size=(61, 61)) for img in foil_images]
                
                target_stimuli, foil_stimuli = foil_stimuli, target_stimuli
                
              

            # Calculate the positions for target and foil stimuli
            y_position = 0  # Adjust as needed

            # Set horizontal positions for target stimuli on the left
            x_offset_target = -300  # Adjust as needed
            spacing_target = 70  # Adjust the horizontal spacing as needed
            for i, target in enumerate(target_stimuli):
                target_x = x_offset_target + (i * spacing_target)
                target.pos = (target_x, y_position)

            # Set horizontal positions for foil stimuli on the right
            x_offset_foil = 200  # Adjust as needed
            spacing_foil = 70  # Adjust the horizontal spacing as needed
            for i, foil in enumerate(foil_stimuli):
                foil_x = x_offset_foil + (i * spacing_foil)
                foil.pos = (foil_x, y_position)

            # Display all target stimuli and foil stimuli
            sound_stim.play()
            for target in target_stimuli:
                target.draw()
            for foil in foil_stimuli:
                foil.draw()

            # Update the window to show the stimuli
            win.flip()
            
        
            
            start_time = core.getTime()
            keys = event.waitKeys(keyList=['left', 'right', 'escape'])
            elapsed_time = core.getTime() - start_time
            #trial[headers.index('Response_Time')] = elapsed_time

            answer = 'left' if 'left' in keys else 'right'
            block_data['Answer'] = answer
            block_data['Accuracy'] = 1 if answer == target_location else 0

            if 'escape' in keys:
                break
                
                
            BLOCK_DATA_TEST.append(block_data)
    
train_block_df = pd.DataFrame(BLOCK_DATA_TRAIN).fillna('-')
train_block_df.to_csv('SOURCE-CSV.csv')

test_block_df = pd.DataFrame(BLOCK_DATA_TEST)
test_block_df.to_csv('Test.csv')
   

# Stop recording
tk.stopRecording()

# Put the tracker to offline mode 
tk.setOfflineMode()

# Close the EDF data file on the Host 
tk.closeDataFile()

# Download the EDF data file from Host
tk.receiveDataFile('psychopy.edf', 'psychopy.edf')

# Close the link to the tracker
tk.close()

# Close the graphics
win.close()
core.quit()
