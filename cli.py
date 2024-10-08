import os
import shutil
from PIL import Image

def create_folders(directory):
    """Create 'good' and 'bad' folders if they don't exist."""
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
    """Display the image using PIL."""
    img = Image.open(image_path)
    img.show()

def main():
    # Step 1: Ask for the directory
    directory = input("Enter the directory path containing images: ")
    
    # Step 2: Navigate to the directory and create 'good' and 'bad' folders
    if not os.path.isdir(directory):
        print(f"Directory {directory} does not exist.")
        return
    
    create_folders(directory)
    good_folder = os.path.join(directory, 'good')
    bad_folder = os.path.join(directory, 'bad')
    
    # Step 3: Get the list of images in the directory
    images = get_images(directory)
    if not images:
        print("No images found in the provided directory.")
        return
    
    # Step 4: Iterate through the images
    for image_name in images:
        image_path = os.path.join(directory, image_name)
        
        # Display the image
        print(f"Displaying: {image_name}")
        display_image(image_path)
        
        # Ask for user input
        while True:
            choice = input("Press 'R' for good, 'L' for bad, or 'Q' to quit: ").upper()
            if choice == 'R':
                move_image(image_path, good_folder)
                print(f"Moved to: {good_folder}")
                break
            elif choice == 'L':
                move_image(image_path, bad_folder)
                print(f"Moved to: {bad_folder}")
                break
            elif choice == 'Q':
                print("Quitting...")
                return
            else:
                print("Invalid input, please try again.")
        
        # Confirm moving the image
        input("Press Enter to continue to the next image...")

    print("No more images left.")

if __name__ == "__main__":
    main()
