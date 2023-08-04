# import os
# import shutil
# import tkinter as tk
# from tkinter import filedialog
# import os
# import shutil


# def get_source_directory():
#     # Create a Tkinter root window
#     root = tk.Tk()
#     # Hide the root window
#     root.withdraw()
#     # Ask the user to select a directory
#     source_dir = filedialog.askdirectory()
#     # Return the selected directory
#     return source_dir

# source_dir = get_source_directory()

# def segregate_files_by_image_position(source_dir):
#     # Create a dictionary to store the destination directories for each image position
#     destination_dirs = {}

#     # Iterate through each file in the source directory
#     for file_name in os.listdir(source_dir):
#         # Get the full path of the file
#         file_path = os.path.join(source_dir, file_name)

#         # Extract the variables from the file name
#         file_parts = os.path.splitext(file_name)[0].split("--")
#         aspect_ratio = file_parts[0]
#         uuid = file_parts[1]
#         product_material = file_parts[2].lower()
#         title_var = file_parts[3]
#         image_position = int(file_parts[4])
#         artist_name = os.path.splitext(file_parts[5])[0].lower()

#         # Create the destination directory for the image position if it doesn't exist
#         if image_position not in destination_dirs:
#             destination_dir = os.path.join(source_dir, f"image_position_{image_position}")
#             os.makedirs(destination_dir, exist_ok=True)
#             destination_dirs[image_position] = destination_dir

#         # Copy the file to the destination directory for the image position
#         destination_dir = destination_dirs[image_position]
#         new_file_name = f"{aspect_ratio}--{uuid}--{product_material}--{title_var}--{image_position}--{artist_name}.jpg"
#         new_file_path = os.path.join(destination_dir, new_file_name)
#         shutil.copy(file_path, new_file_path)

# # Create the root window
# root = tk.Tk()

# # Create the Extract Files button
# extract_files_button = tk.Button(root, text="Extract Files", command=segregate_files_by_image_position(source_dir))
# extract_files_button.pack(pady=10)

# # Run the Tkinter event loop
# root.mainloop()