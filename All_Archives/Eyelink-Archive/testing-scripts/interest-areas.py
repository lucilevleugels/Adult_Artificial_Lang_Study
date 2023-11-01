# Import necessary libraries
from psychopy import visual, core, event

# Create a window
SCN_W, SCN_H = (1280, 800)

# Open a Psychopy window with the "allowStencil" option 
win = visual.Window((SCN_W, SCN_H), fullscr=False, units='pix', allowStencil=True, color=(1, 1, 1))

# Load the cube image
cube_image = visual.ImageStim(win, image='cube.png', size=(61, 61))

# Define positions for the cube image
positions = {
    'left': (-400, 0),
    'right': (400, 0),
    'top': (0, 300),
    'center': (0, -300),
}

# Initialize the position index
position_index = 0

escape_key = 'escape'
space_key = 'space'
escape_pressed = False

while position_index < len(positions):
    position_name = list(positions.keys())[position_index]
    position = list(positions.values())[position_index]
    cube_image.pos = position
    cube_image.draw()
    win.flip()

    # Wait for the Spacebar key press to move to the next position
    keys = event.waitKeys(keyList=[space_key, escape_key])
    if space_key in keys:
        position_index += 1
    elif escape_key in keys:
        escape_pressed = True
        break

# Close the window
win.close()
