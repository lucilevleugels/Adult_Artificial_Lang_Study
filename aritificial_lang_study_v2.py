from psychopy import visual, core, sound, event, gui, data
import os, csv
import pandas as pd 


# 1 . Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["correlated","isolated-left","isolated-center","isolated-right"])
choice_data = choice_dialog.show()

print()


SCN_W, SCN_H = (1280, 800)
# Open a PsyhocPy window with the "allowStencil" option 
win = visual.Window(fullscr=True, units='pix', allowStencil=True, color=(1,1,1))


train_df = pd.read_csv('Trial_Info/train_v3.csv')
test_df = pd.read_csv('Trial_Info/test_v3.csv')



# df by condition
train_dfs = {}
for condition in train_df['condition'].unique():
        train_dfs[condition] = train_df[train_df['condition']==condition]
        
test_dfs = {}
for condition in test_df['condition'].unique():
        test_dfs[condition] = test_df[test_df['condition']==condition]




training_phase_text = visual.TextStim(win, text="Training Phase", height=20, color=(-1, -1, -1), pos=(0,0))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=20 , color=(-1, -1, -1), pos=(0,0))

#BLOCK DICTIONARY

BLOCK_DATA_TRAIN = []
BLOCK_DATA_TEST = []

for iteration in range(1):
    
    
    train_trial_df = train_dfs[choice_data[0]].sample(frac=1)
    test_trial_df = test_dfs[choice_data[0]].sample(frac=1)

    
    

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
            sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]

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
            for image_stim in image_stims:
                image_stim.draw()
                
            win.flip()
            
            for sound_stim in sound_stims:
                sound_stim.play()
                core.wait(0.6)
                
           
                
            
            BLOCK_DATA_TRAIN.append(block_data)
            keys = event.waitKeys(keyList=['space']) 
            

    
    #print(BLOCK_DATA_TRAIN)
        
      
    #TESTING PHASE
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
            sound_stims = [sound.Sound(audio_path) for audio_path in audio_paths]
            
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
            for target in target_stimuli:
                target.draw()
            for foil in foil_stimuli:
                foil.draw()
                
            # Update the window to show the stimuli
            win.flip()
            
            for sound_stim in sound_stims:
                sound_stim.play()
                core.wait(0.8)
            
            
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
train_block_df.to_csv('Train-Block-Source.csv')

test_block_df = pd.DataFrame(BLOCK_DATA_TEST)
test_block_df.to_csv('Testing-Data.csv')




    