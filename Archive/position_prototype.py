from psychopy import visual, core, event
import pandas as pd

# Create a window
SCN_W, SCN_H = (1280, 800)
# Open a PsyhocPy window with the "allowStencil" option 
win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', allowStencil=True, color=(1,1,1))

CODITION = 1

test_df = pd.read_csv('../Trial_Info/Testing_Trials_Adult_Lang_Study.csv')

for row in test_df.iterrows():
    trial_data = row[1]
    
    target_images = trial_data['Target_image'].split(',')
    foil_images = trial_data['Foil_image'].split(',')
    
    print('target', target_images)
    print('foil images', foil_images)
    print('-'*25)

    # Create image stimuli for target and foil images
    target_stimuli = [visual.ImageStim(win, image=img.strip(), size=(62, 61)) for img in target_images]
    foil_stimuli = [visual.ImageStim(win, image=img.strip(), size=(62, 61)) for img in foil_images]

   # Calculate the positions for target and foil stimuli
    y_position = 0  # Adjust as needed

    # Set horizontal positions for target stimuli on the left
    x_offset_target = -150  # Adjust as needed
    spacing_target = 70  # Adjust the horizontal spacing as needed
    for i, target in enumerate(target_stimuli):
        target_x = x_offset_target + (i * spacing_target)
        target.pos = (target_x, y_position)

    # Set horizontal positions for foil stimuli on the right
    x_offset_foil = 150  # Adjust as needed
    spacing_foil = 70  # Adjust the horizontal spacing as needed
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

    # Wait for a key press to exit
    event.waitKeys()

# Close the window
win.close()
core.quit()
