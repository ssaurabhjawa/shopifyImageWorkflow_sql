import os
import shutil
import tkinter as tk
from tkinter import filedialog
from extract_file_info_v5 import extract_file_info_v5

def move_images_to_new_location():
    # Prompt user to select source directory
    root = tk.Tk()
    root.withdraw()
    source_dir = filedialog.askdirectory(title="Select Source Directory")

    # Set destination directory
    dest_dir = r"D:\OBLJJAWA\My Drive\Products"

    # Create destination directory if it doesn't exist
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # Loop through all files in source directory
    for file_name in os.listdir(source_dir):
        # Check if file is an image
        if file_name.endswith(".jpg") or file_name.endswith(".png"):
            # Extract file info
            file_path = os.path.join(source_dir, file_name)
            file_info = extract_file_info_v5(file_path)
            if file_info is None:
                continue

            # Create product folder in destination directory if it doesn't exist
            product_folder_name = f"{file_info['handle']} - {file_info['title']}"
            product_folder_path = os.path.join(dest_dir, product_folder_name)
            if not os.path.exists(product_folder_path):
                os.makedirs(product_folder_path)

            # Move file to product folder
            dest_file_path = os.path.join(product_folder_path, file_name)
            shutil.move(file_path, dest_file_path)