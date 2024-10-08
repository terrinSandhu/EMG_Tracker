import os
import shutil
from PIL import Image
from pynput import keyboard

# Global variables to track which key was pressed and to exit the loop
key_pressed = None
move_confirmed = False
exit_program = False

def ask_for_directory():
    """Prompt the user to provide a directory."""
    directory = input("Please enter the directory containing images: ")
    if not os.path.isdir(directory):
        print(f"The directory '{directory}' does not exist. Please try again.")
        return ask_for_directory()
    return directory

def create_folders(base_dir):
    """Create 'good' and 'bad' folders if they don't already exist."""
    good_folder = os.path.join(base_dir, 'good')
    bad_folder = os.path.join(base_dir, 'bad')
    os.makedirs(good_folder, exist_ok=True)
    os.makedirs(bad_folder, exist_ok=True)
    return good_folder, bad_folder

def list_images(folder):
    """List all image files in the folder."""
    return [f for f in os.listdir(folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

def move_image(image_path, destination_folder):
    """Move the image to the specified destination folder."""
    shutil.move(image_path, destination_folder)

def open_image(image_path):
    """Open the image using PIL's Image."""
    img = Image.open(image_path)
    img.show()

def on_press(key):
    global key_pressed, move_confirmed, exit_program
    try:
        if key == keyboard.Key.right:
            key_pressed = 'good'
        elif key == keyboard.Key.left:
            key_pressed = 'bad'
        elif key == keyboard.Key.enter:
            move_confirmed = True
        elif key == keyboard.Key.esc:
            exit_program = True
            return False  # Stop listener when 'esc' is pressed
    except AttributeError:
        pass

def image_sorter(images, source_folder, good_folder, bad_folder):
    global key_pressed, move_confirmed, exit_program
    idx = 0

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    while idx < len(images) and not exit_program:
        current_image = os.path.join(source_folder, images[idx])
        
        # Open the current image
        open_image(current_image)
        print(f"\nCurrent image: {images[idx]}")
        print("Press the right arrow to move to 'good', left arrow for 'bad'.")
        print("Press 'Enter' to confirm moving the image.")
        print("Press 'Esc' to quit.")

        # Wait for the user to press right or left arrow and confirm with Enter
        while not move_confirmed and not exit_program:
            if key_pressed == 'good':
                print("Selected 'good'. Press 'Enter' to confirm.")
            elif key_pressed == 'bad':
                print("Selected 'bad'. Press 'Enter' to confirm.")

        # Move the image if confirmed
        if move_confirmed and key_pressed:
            if key_pressed == 'good':
                move_image(current_image, good_folder)
                print(f"Moved '{images[idx]}' to 'good'.")
            elif key_pressed == 'bad':
                move_image(current_image, bad_folder)
                print(f"Moved '{images[idx]}' to 'bad'.")
            
            # Reset for next image
            idx += 1
            key_pressed = None
            move_confirmed = False

    listener.stop()

    if idx >= len(images):
        print("All images have been sorted. No images left.")

def main():
    # Ask for the directory containing images
    source_folder = ask_for_directory()

    # Create 'good' and 'bad' folders
    good_folder, bad_folder = create_folders(source_folder)

    # List all the images in the source folder
    images = list_images(source_folder)

    if not images:
        print("No images found in the directory.")
        return

    # Start sorting images
    image_sorter(images, source_folder, good_folder, bad_folder)

if __name__ == "__main__":
    main()
