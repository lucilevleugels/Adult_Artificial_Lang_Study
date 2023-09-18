# Adult_Artificial_Lang_Study

Background & Significance of the study:
The study examines if a more systematic language structure, like chinese, facilitates more efficient learning compared to less systematic languages, like English. By observing learners' eye movements and behavior, the research aims to understand how language structure influences the learning process in real-time. This research will enhance our knowledge of how language systems affect attention and learning, with implications for future educational strategies.

Overview: 
This script has been designed to conduct an adult language systematicity study using PsychoPy. Participants will be presented with audio stimuli and visual images across multiple training and testing phases. 

Structure: 

Setup: A window is initiated with a white background. Trials are loaded from CSV files detailing the stimuli and expected responses. 

Condition Selection: Before beginning the experiment, the user selects between two conditions: "Condition 1" and "Condition 2". This choice determines the set of stimuli to be used. 
    
Main Experiment: The study is divided into iterations of training and testing phases, which will repeat four times. Before each phase, a label ("Training Phase" or "Testing Phase") is displayed to cue the participant. 
        
Training Phase: The participant listens to an audio stimulus while being presented with a set of images. After the audio plays, the user presses the spacebar to progress to the next trial. 
        
Testing Phase: The participant listens to an audio stimulus and then selects an image (either on the left or right) that they believe corresponds to the audio. Their choice (left or right) is recorded, along with the time it took them to make that choice. Pressing the 'escape' key at any point during this phase will terminate the experiment. 
        
Data Saving: At the end of each testing phase, the participant's responses and reaction times are saved back to the CSV.

Audio: wav files produced from natural reader.

Images: From Truk-Browne etl al (2008) 
