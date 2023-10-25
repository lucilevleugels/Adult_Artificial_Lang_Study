from psychopy import visual, core, sound, event, gui, data
import os, csv
import pandas as pd 


# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["Condition 1", "Condition 2"])
choice_data = choice_dialog.show()


SCN_W, SCN_H = (1280, 800)
# Open a PsyhocPy window with the "allowStencil" option 
win = visual.Window(fullscr=True, units='pix', allowStencil=True, color=(1,1,1))


train_df = pd.read_csv('Trial_Info/Training_Trails_Adult_Lang_Study.csv')
test_df = pd.read_csv('Trial_Info/Testing_Trials_Adult_Lang_Study.csv')



training_phase_text = visual.TextStim(win, text="Training Phase", height=20, color=(-1, -1, -1), pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=20 , color=(-1, -1, -1), pos=(0,0))

#BLOCK DICTIONARY

BLOCK_DATA_TRAIN = []
BLOCK_DATA_TEST = []

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
            
    
    
    #print(BLOCK_DATA_TRAIN)
        
      
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
                
#                
#            # Calculate the positions for target and foil stimuli
#            y_position = 0  # Adjust as needed
#            
#            # Calculate the total width of the target and foil stimuli based on the window size
#            total_target_width = len(target_stimuli) * 70  # Adjust the horizontal spacing as needed
#            total_foil_width = len(foil_stimuli) * 70  # Adjust the horizontal spacing as needed
#
#
#            # Calculate the total width of the target and foil stimuli based on the window size
#            win_width = 1280
#            # Calculate the starting positions to center the stimuli based on the window size
#            x_start_target = -(total_target_width + total_foil_width) / 2 + win_width / 2
#
#            # Set horizontal positions for target stimuli
#            for i, target in enumerate(target_stimuli):
#                target_x = x_start_target + (i * 70)  # Adjust the horizontal spacing as needed
#                target.pos = (target_x, y_position)
#
#            # Set horizontal positions for foil stimuli
#            for i, foil in enumerate(foil_stimuli):
#                foil_x = x_start_target + (total_target_width / 2) + (i * 70)  # Adjust the horizontal spacing as needed
#                foil.pos = (foil_x, y_position)
#
#            # Display all target stimuli and foil stimuli
#            for target in target_stimuli:
#                target.draw()
#            for foil in foil_stimuli:
#                foil.draw()


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
            block_data['Response Time'] = elapsed_time

            answer = 'left' if 'left' in keys else 'right'
            block_data['Answer'] = answer
            block_data['Accuracy'] = 1 if answer == target_location else 0
            
            BLOCK_DATA_TEST.append(block_data)

            
            if 'escape' in keys:
                break
                
                
            
            
        
                    
                
train_block_df = pd.DataFrame(BLOCK_DATA_TRAIN).fillna('-')
train_block_df.to_csv('SOURCE-CSV.csv')

test_block_df = pd.DataFrame(BLOCK_DATA_TEST)
test_block_df.to_csv('Test.csv')




    