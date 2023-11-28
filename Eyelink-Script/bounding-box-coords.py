def convert_psychopy_to_eyelink(psychopy_coords, screen_resolution):
    """
    Convert PsychoPy coordinates to EyeLink coordinates.

    :param psychopy_coords: A list of tuples, where each tuple represents a PsychoPy (x, y) coordinate.
    :param screen_resolution: A tuple representing the EyeLink screen resolution (width, height).
    :return: A list of tuples representing the converted EyeLink coordinates.
    """
    screen_width, screen_height = screen_resolution
    center_x, center_y = screen_width // 2, screen_height // 2

    # Convert PsychoPy coordinates to EyeLink coordinates
    eyelink_coords = [(x + center_x, center_y - y) for x, y in psychopy_coords]
    return eyelink_coords

# Example usage:
psychopy_coords_example = [(-350, 0), (0, 0), (350, 0)]  # PsychoPy coordinates
screen_resolution_example = [3840, 2160]# EyeLink screen resolution

# Convert and print the coordinates
eyelink_coords_example = convert_psychopy_to_eyelink(psychopy_coords_example, screen_resolution_example)
print(eyelink_coords_example)
