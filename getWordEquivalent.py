import os
import shutil
import tkinter as tk
from tkinter import filedialog

import os
import shutil

def extract_file_info(file_path):
    # Extract file name from file path
    file_name = os.path.basename(file_path)
    # Split file name into parts based on delimiter
    file_parts = file_name.split("--")

    # Check if the file name has the expected number of parts
    if len(file_parts) < 6:
        # Handle the error gracefully (you can choose to log the error or skip the file)
        print(f"Error: Invalid filename format for {file_name}")
        return None

    # Extract variables from file parts
    aspect_ratio = (file_parts[0])
    uuid = file_parts[1]
    product_material = file_parts[2].lower()
    title_var = file_parts[3]
    image_position_var = int(file_parts[4])
    artist_name = os.path.splitext(file_parts[5])[0].lower()

    # Create dictionary containing the extracted variables
    file_info = {
        "aspect_ratio": float(aspect_ratio),
        "handle": uuid,
        "title": title_var,
        "image_position_var": image_position_var,
        "vendor": artist_name,
        "product_material": product_material,
    }

    return file_info["image_position_var"]



def get_word_equivalent(number):
    # Define a dictionary mapping numbers to word equivalents
    word_equivalents = {
        0: "zero",
        1: "one",
        2: "two",
        3: "three",
        4: "four",
        5: "five",
        6: "six",
        7: "seven",
        8: "eight",
        9: "nine"
    }
    # Return the word equivalent of the number
    return word_equivalents.get(number, str(number))


def segregate_image_position():
    # Ask the user to select a directory containing images
    source_dir = filedialog.askdirectory()

    # Set the destination directory to a subdirectory of the source directory
    destination_dir = os.path.join(source_dir, "segregated_images")
    # Create the destination directory if it doesn't exist
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Iterate through each file in the source directory
    for file_name in os.listdir(source_dir):
        # Get the full path of the file
        file_path = os.path.join(source_dir, file_name)
        # Extract the aspect ratio from the file name
        image_position = extract_file_info(file_path)
        if image_position is None:
            continue
        # Create the aspect ratio folder if it doesn't exist
        image_position_dir = os.path.join(destination_dir, str(image_position))
        if not os.path.exists(image_position_dir):
            os.makedirs(image_position_dir)
        # Get the word equivalent of the image position
        word_equivalent = get_word_equivalent(image_position)
        # Rename the file with the word equivalent of the image position
        new_file_name = file_name.replace(str(image_position), word_equivalent)
        new_file_path = os.path.join(image_position_dir, new_file_name)
        # Copy the file to the aspect ratio folder
        shutil.copy(file_path, new_file_path)



# Create the root window
root = tk.Tk()

# Create the Extract Files button
extract_files_button = tk.Button(root, text="Extract Files", command=segregate_image_position)
extract_files_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()