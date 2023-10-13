# Trial Segmentation 
'''
TRIALID <values that help to identify a trial>
TRIAL_RESULT <values representing possible trial result>
'''

import pylink
# Connect to the tracker
tk = pylink.EyeLink()
# Open an EDF on the Host
# filename must not exceed 8 characters
tk.openDataFile('seg.edf')


# Run through five trials
for trial in range(1, 6):
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
    
     # Send TRIAL_VAR messages to store variables in the EDF
    tk.sendMessage('!V TRIAL_VAR condition step')
    tk.sendMessage('!V TRIAL_VAR gap_duration 200')
    tk.sendMessage('!V TRIAL_VAR direction Right')m
    
    
    # Log a TRIAL_RESULT message to mark trial ends
    tk.sendMessage('TRIAL_RESULT 0')
    
# Wait for 100 to catch session end events
pylink.msecDelay(100)
# Close the EDF file and download it from the Host PC
tk.closeDataFile()
tk.receiveDataFile('seg.edf', 'trial_segmentation_demo.edf')
# Close the link
tk.close()

