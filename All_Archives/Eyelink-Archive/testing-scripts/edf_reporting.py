# Trial Segmentation 
'''
TRIALID <values that help to identify a trial>
TRIAL_RESULT <values representing possible trial result>
'''

import pylink
from psychopy import visual, core, event

# Create a window
# Screen resolution
SCN_W, SCN_H = (2280, 1580)
# Open a PsyhocPy window
win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', color='white')

#

# Connect to the tracker
tk = pylink.EyeLink()
# Open an EDF on the Host
# filename must not exceed 8 characters
tk.openDataFile('seg.edf')


# Run through five trials
for trial in range(1):
# Print out a message to show the current trial 
    print(f'Trial #: {trial}')
    
    # Log a TRIALID message to mark trial start
    tk.sendMessage(f'TRIALID {trial}')
    # Start recording
    tk.startRecording(1, 1, 1, 1)
    # Pretending that we are doing something for 2-sec
    pylink.pumpDelay(2000)
    # Stop recording
    tk.stopRecording()
    
#     # Send TRIAL_VAR messages to store variables in the EDF
#    tk.sendMessage('!V TRIAL_VAR condition step')
#    tk.sendMessage('!V TRIAL_VAR gap_duration 200')
#    tk.sendMessage('!V TRIAL_VAR direction Right')
    
    image = visual.ImageStim(win, image='cube.png')

    # Define the coordinates
    coordinates = [(-150, 0), (0, 0), (150, 0)]
    current_coordinate = 0

    # Create a TextStim to display instructions
    instruction_text = visual.TextStim(win, text="Press Space to continue")

    # Main loop
    while True:
        # Check for a spacebar press
        if 'space' in event.getKeys():
            current_coordinate += 1
            if current_coordinate >= len(coordinates):
                break

        # Set the image position
        image.pos = coordinates[current_coordinate]

        # Clear the window
        win.flip()

    # Close the window
    win.close()
    
    
    tk.sendMessage("!V IAREA RECTANGLE 1 -150 0 -50 100 image1")
    tk.sendMessage("!V IAREA RECTANGLE 2 0 0 100 100 image2")
    tk.sendMesage("!V IAREA RECTANGLE 3 50 0 150 100 image3")
    
    # Log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')
    
# Wait for 100 to catch session end events
pylink.msecDelay(100)
# Close the EDF file and download it from the Host PC
tk.closeDataFile()
tk.receiveDataFile('seg.edf', 'bounding_box.edf')
# Close the link
tk.close()

