import os
import shutil
import tkinter as tk
from tkinter import filedialog

import os
import shutil

def extract_file_info(file_path):
    # Split file name into parts based on delimiter
    file_parts = os.path.splitext(os.path.basename(file_path))[0].split("--")

    # Extract variables from file parts
    aspect_ratio = float(file_parts[0])

    # Return the extracted variables
    return aspect_ratio


def extract_files_button_clicked():
    # Ask the user to select a directory containing images
    source_dir = filedialog.askdirectory()

    # Set the destination directory to the same directory as the source directory
    destination_dir = source_dir



def segregate_aspect_ratio():
    # Ask the user to select a directory containing images
    source_dir = filedialog.askdirectory()

    # Set the destination directory to the same directory as the source directory
    destination_dir = source_dir
    # Iterate through each file in the source directory
    for file_name in os.listdir(source_dir):
        # Get the full path of the file
        file_path = os.path.join(source_dir, file_name)
        # Extract the aspect ratio from the file name
        aspect_ratio = extract_file_info(file_path)
        # Create the aspect ratio folder if it doesn't exist
        aspect_ratio_dir = os.path.join(destination_dir, str(aspect_ratio))
        if not os.path.exists(aspect_ratio_dir):
            os.makedirs(aspect_ratio_dir)
        # Copy the file to the aspect ratio folder
        shutil.copy(file_path, aspect_ratio_dir)

# Create the root window
root = tk.Tk()

# Create the Extract Files button
extract_files_button = tk.Button(root, text="Extract Files", command=segregate_aspect_ratio)
extract_files_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()