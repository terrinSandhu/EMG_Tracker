import os
import shutil
from PIL import Image
import curses

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

def image_sorter(stdscr, images, source_folder, good_folder, bad_folder):
    """Handle the image sorting functionality using curses."""
    curses.curs_set(0)  # Hide the cursor
    idx = 0  # Start with the first image
    
    while idx < len(images):
        current_image = os.path.join(source_folder, images[idx])
        
        # Open the current image
        open_image(current_image)

        stdscr.clear()
        stdscr.addstr(0, 0, f"Current image: {images[idx]}")
        stdscr.addstr(1, 0, "Press the right arrow to move to 'good', left arrow for 'bad'.")
        stdscr.addstr(2, 0, "Press 'Enter' to confirm moving the image.")
        stdscr.addstr(3, 0, "Press 'q' to quit.")
        
        # Capture the key press
        key = stdscr.getch()

        destination = None

        # If left arrow key, prepare to move to 'bad'
        if key == curses.KEY_LEFT:
            destination = bad_folder

        # If right arrow key, prepare to move to 'good'
        elif key == curses.KEY_RIGHT:
            destination = good_folder

        # If 'q' is pressed, quit the program
        elif key == ord('q'):
            break

        # If destination is set (left or right arrow pressed)
        if destination:
            stdscr.addstr(4, 0, "Press 'Enter' to confirm.")
            stdscr.refresh()
            confirmation = stdscr.getch()

            if confirmation == ord('\n'):
                move_image(current_image, destination)
                stdscr.addstr(5, 0, f"Moved '{images[idx]}' to '{destination}'")
                idx += 1

        stdscr.refresh()

    # Once all images are sorted
    stdscr.clear()
    stdscr.addstr(0, 0, "All images have been sorted. No images left.")
    stdscr.refresh()
    stdscr.getch()  # Wait for any key to exit

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

    # Initialize curses to handle the sorting process
    curses.wrapper(image_sorter, images, source_folder, good_folder, bad_folder)

if __name__ == "__main__":
    main()
