def calculate_bounding_boxes(image_coords, image_size, screen_resolution):
    """
    Calculate the bounding box coordinates for images given their center points.

    :param image_coords: A list of tuples, where each tuple represents the center (x, y) coordinate of an image.
    :param image_size: A tuple representing the size (width, height) of the images.
    :param screen_resolution: A tuple representing the screen resolution (width, height).
    :return: A list of tuples representing the top-left and bottom-right coordinates of the bounding boxes.
    """
    # Calculate the half width and half height of the images
    half_width = image_size[0] // 2
    half_height = image_size[1] // 2

    # Calculate bounding boxes
    bounding_boxes = []
    for center_x, center_y in image_coords:
        top_left = (center_x - half_width, center_y - half_height)
        bottom_right = (center_x + half_width, center_y + half_height)
        bounding_boxes.append((top_left, bottom_right))

    return bounding_boxes

# Image coordinates and screen resolution
image_coords_list = [(1570, 1080), (1920, 1080), (2270, 1080)]
image_size = (350, 351)
screen_resolution = (3840, 2160)

# Get bounding box coordinates
bounding_box_coords = calculate_bounding_boxes(image_coords_list, image_size, screen_resolution)

# Print out the bounding box coordinates
for index, bbox in enumerate(bounding_box_coords, start=1):
    print(f"Image{index} Bounding Box: Top Left {bbox[0]}, Bottom Right {bbox[1]}")

print()
print("Bounding Box Coordinates Top Left to Bottom Right")
print(bounding_box_coords)  # Return the list if needed
