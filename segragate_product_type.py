import os
import shutil
import tkinter as tk
from tkinter import filedialog

def extract_file_info(file_path):
    # Extract file name from file path
    file_name = os.path.basename(file_path)
    # Split file name into parts based on delimiter
    file_parts = file_name.split("--")

    # Extract variables from file parts
    aspect_ratio = float(file_parts[0])
    uuid = file_parts[1]
    product_type = file_parts[2].lower()
    title_var = file_parts[3]
    image_position_var = int(file_parts[4])
    artist_name = os.path.splitext(file_parts[5])[0].lower()

    # Return the extracted variables
    return aspect_ratio, uuid, product_type, title_var, image_position_var, artist_name

def extract_files_button_clicked():
    # Ask the user to select a directory containing images
    source_dir = filedialog.askdirectory()

    # Set the destination directory to the same directory as the source directory
    destination_dir = source_dir

    # Iterate through each file in the source directory
    for file_name in os.listdir(source_dir):
        # Get the full path of the file
        file_path = os.path.join(source_dir, file_name)
        # Extract the product type from the file name
        product_type = extract_file_info(file_path)[2]
        # Create the product type folder if it doesn't exist
        product_dir = os.path.join(destination_dir, product_type)
        if not os.path.exists(product_dir):
            os.makedirs(product_dir)
        # Copy the file to the product folder
        shutil.copy(file_path, product_dir)

# Create the root window
root = tk.Tk()

# Create the Extract Files button
extract_files_button = tk.Button(root, text="Extract Files", command=extract_files_button_clicked)
extract_files_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()