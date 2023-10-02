# 1. Setup
from psychopy import visual, core, sound, event, gui, data
import os, csv

win = visual.Window([800, 600], monitor="testMonitor", units="deg", color=(1, 1, 1))
#SCN_W, SCN_H = (1280, 800)
## Open a PsyhocPy window with the "allowStencil" option 
#win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', allowStencil=True, color=(1,1,1))

mouse = event.Mouse(win=win)
condition_selected = None

# Load trial information from CSV
trial_info = []
with open('Trial_Info/Training_Trails_Adult_Lang_Study.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # skip header
    for row in csvreader:
        trial_info.append(row)

# 2. Condition Selection
choice_dialog = gui.Dlg(title="Select a Condition")
choice_dialog.addField("Condition:", choices=["Condition 1", "Condition 2"])
choice_data = choice_dialog.show()
if choice_data[0] == "Condition 1":
    condition_selected = 3
else:
    condition_selected = 4

training_phase_text = visual.TextStim(win, text="Training Phase", height=1.1, color=(-1, -1, -1))
testing_phase_text = visual.TextStim(win, text="Testing Phase", height=1.1, color=(-1, -1, -1))

for iteration in range(4):

    # Display "Training Phase"
    training_phase_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])  # Wait for spacebar press to continue

    # 3. Main Loop (Training Phase)
    for trial in trial_info:
        audio_name = trial[condition_selected]
        audio_path = os.path.join('Audio', audio_name + '.wav')
        sound_stim = sound.Sound(audio_path)
    
        images = trial[5].split(', ')
        image_stims = [visual.ImageStim(win, image=os.path.join('Images', image_name.strip())) for image_name in images]
    
        # Aligning images
        total_images = len(image_stims)
        if total_images % 2 == 0:
            half = total_images // 2
            positions = range(-half + 1, half + 1)
        else:
            positions = range(-total_images // 2, total_images // 2 + 1)

        for stim, pos in zip(image_stims, positions):
            stim.pos = [pos * 1.5, 0]
    
        sound_stim.play()
        for stim in image_stims:
            stim.draw()
        win.flip()
    
        keys = event.waitKeys(keyList=['space'])

    # Display "Testing Phase"
    testing_phase_text.draw()
    win.flip()
    event.waitKeys(keyList=['space'])  # Wait for spacebar press to continue

    # Start Testing Phase
    testing_info = []
    with open('Trial_Info/Testing_Trials_Adult_Lang_Study.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        headers = next(csvreader)
        for row in csvreader:
            testing_info.append(row)

    # Testing phase
    for trial in testing_info:
        if condition_selected == 3:
            audio_name = trial[headers.index('Target_audio_cond1')]
        else:
            audio_name = trial[headers.index('Target_audio_cond2')]

        audio_path = os.path.join('Audio', audio_name + '.wav')
        sound_stim = sound.Sound(audio_path)

        target_images = trial[headers.index('Target_image')].split(', ')
        foil_images = trial[headers.index('Foil_image')].split(', ')

        target_stims = [visual.ImageStim(win, image=os.path.join('Images', image_name.strip())) for image_name in target_images]
        foil_stims = [visual.ImageStim(win, image=os.path.join('Images', image_name.strip())) for image_name in foil_images]

        # Position images based on 'Target_Location'
        target_position = -1.5 if trial[headers.index('Target_Location')] == "left" else 1.5
        foil_position = 1.5 if trial[headers.index('Target_Location')] == "left" else -1.5

        for stim in target_stims:
            stim.pos = [target_position, 0]
            stim.draw()
        for stim in foil_stims:
            stim.pos = [foil_position, 0]
            stim.draw()

        sound_stim.play()
        win.flip()

        start_time = core.getTime()
        keys = event.waitKeys(keyList=['left', 'right', 'escape'])
        elapsed_time = core.getTime() - start_time
        trial[headers.index('Response_Time')] = elapsed_time

        answer = 'left' if 'left' in keys else 'right'
        trial[headers.index('Answer')] = answer

        if 'escape' in keys:
            break

    # Save updated CSV with participants' answers
    with open('Trial_Info/Testing_Trials_Adult_Lang_Study.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(headers)
        csvwriter.writerows(testing_info)

win.close()
core.quit()
