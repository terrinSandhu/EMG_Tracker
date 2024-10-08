import os
import shutil
from PIL import Image
from pynput import keyboard

# Global variables to keep track of the current image and its directory
current_image_index = 0
images = []
directory = ""
good_folder = ""
bad_folder = ""
move_direction = None
image_open = None

def create_folders(directory):
    """Create 'good' and 'bad' folders if they don't exist."""
    global good_folder, bad_folder
    good_folder = os.path.join(directory, 'good')
    bad_folder = os.path.join(directory, 'bad')
    
    if not os.path.exists(good_folder):
        os.makedirs(good_folder)
    if not os.path.exists(bad_folder):
        os.makedirs(bad_folder)

def get_images(directory):
    """Return a list of image files in the directory."""
    supported_formats = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    return [f for f in os.listdir(directory) if f.lower().endswith(supported_formats)]

def move_image(image_path, target_folder):
    """Move the image to the target folder."""
    shutil.move(image_path, target_folder)

def display_image(image_path):
    """Display the image using PIL and ensure it closes after viewing."""
    global image_open
    image_open = Image.open(image_path)
    image_open.show()

def on_press(key):
    global current_image_index, move_direction, image_open

    try:
        if key == keyboard.Key.right:
            move_direction = 'good'
            print("Right key pressed. Image will be moved to 'good'.")
            confirm_and_move()
        elif key == keyboard.Key.left:
            move_direction = 'bad'
            print("Left key pressed. Image will be moved to 'bad'.")
            confirm_and_move()
        elif key == keyboard.Key.esc:
            print("Exiting...")
            return False
    except AttributeError:
        pass

def confirm_and_move():
    global current_image_index, images, directory, move_direction, image_open

    if move_direction == 'good':
        move_image(os.path.join(directory, images[current_image_index]), good_folder)
    elif move_direction == 'bad':
        move_image(os.path.join(directory, images[current_image_index]), bad_folder)

    # Close the image before moving to the next one
    if image_open:
        image_open.close()

    current_image_index += 1
    if current_image_index < len(images):
        display_next_image()
    else:
        print("No more images left.")
        return False

def display_next_image():
    global current_image_index, images, directory
    image_path = os.path.join(directory, images[current_image_index])
    print(f"Displaying: {images[current_image_index]}")
    display_image(image_path)

def main():
    global directory, images

    # Step 1: Ask for the directory
    directory = input("Enter the directory path containing images: ")
    
    # Step 2: Navigate to the directory and create 'good' and 'bad' folders
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    create_folders(directory)

    # Step 3: Get the list of images in the directory
    images = get_images(directory)
    if not images:
        print("No images found in the provided directory.")
        return
    
    # Step 4: Display the first image and start listening for keyboard inputs
    display_next_image()

    # Start listening for keyboard input for left (bad) and right (good) key presses
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
