import os
from tkinter import Tk
from tkinter.filedialog import askdirectory

def fix_aspect_ratio():
    # Prompt the user to select a folder
    root = Tk()
    root.withdraw()
    folder_path = askdirectory()

    # Define aspect ratio ranges and create folders
    aspect_ratios = {
        (0.0, 0.71): '0.67',
        (0.71, 0.75): '0.71',
        (0.75, 0.8): '0.75',
        (0.8, 0.9): '0.8',
        (1, 1.2): '1.00',
        (1.2, 1.33): '1.25',
        (1.33333, 1.4): '1.3',
        (1.4, 1.5): '1.4',
        (1.5, 2): '1.5',
    }


    for file_name in os.listdir(folder_path):
        if file_name.endswith(".jpg") or file_name.endswith(".jpeg") or file_name.endswith(".png")  or file_name.endswith(".gif") or file_name.endswith(".webp"):
            file_path = os.path.join(folder_path, file_name)

            # Get the aspect ratio from the file name
            parts = file_name.split("--")
            aspect_ratio = parts[-2]
            if aspect_ratio == "1.0":
                parts[-2] = "1.00"
                new_file_name = "--".join(parts)
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(file_path, new_file_path)

fix_aspect_ratio()