import tkinter as tk
from tkinter import filedialog, messagebox
import tinify
from dotenv import load_dotenv
import os

# Create the root window
root = tk.Tk()
root.title("Image Optimization")

# Configure rows and columns with grid_columnconfigure and grid_rowconfigure
for i in range(8):
    root.grid_columnconfigure(i, weight=1, minsize=50)
    root.grid_rowconfigure(i, weight=1, minsize=50)

# Create widgets with grid
for i in range(11):
    for j in range(4):
        label = tk.Label(root, text=f"({i}, {j})", borderwidth=1, relief="solid")
        label.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")


# Load environment variables from .env file
load_dotenv()



#==================================================================
#                   Ask for directory
#==================================================================
# Create listbox to display files
file_listbox = tk.Listbox(root, width=100, height=100)
file_listbox.grid(row=1, column=1, padx=10, pady=5)

def ask_directory():
    """Ask the user to select a directory."""
    global directory
    directory = filedialog.askdirectory()
    if directory:
        refresh_file_list(directory)
    return directory

def refresh_file_list(directory):
    # Clear existing items in the listbox
    file_listbox.delete(0, tk.END)
    # Get a list of files in the directory
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    # Filter the list of files to include only image files
    image_files = [f for f in files if f.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'))]
    # Insert image files into the listbox
    for file in image_files:
        file_listbox.insert(tk.END, file)

def refresh_button_clicked():
    """Called when the Refresh button is clicked."""
    if directory:
        refresh_file_list(directory)

# Create the Select Directory button
select_directory_button = tk.Button(root, text="Select Directory", command=ask_directory)
select_directory_button.grid(row=0, column=1, pady=10)

# Create the Refresh button
refresh_button = tk.Button(root, text="Refresh", command=refresh_button_clicked)
refresh_button.grid(row=0, column=1, pady=10, sticky="e")

#==================================================================
#                  Tinify
#==================================================================
# Configure Tinify API key
try:
    tinify.key = os.getenv("TINIFY_API_KEY")
    tinify.validate()
except tinify.Error as e:
    # Validation of API key failed.
    pass

def compress_image(image_source, output_file_path):
    try:
        image_file_name = os.path.basename(image_source)
        
        if image_source.startswith('https'):
            source = tinify.from_url(image_source)
        else:
            source = tinify.from_file(image_source)
        print('{0} compressed successfully'.format(image_file_name))        
    except tinify.AccountError:
        print('Invalid API Key')
        return False
    except tinify.ConnectionError:
        print('Please check your internet connection')
        return False
    except tinify.ClientError:
        print('File type is not supported')
        return False
    else:
        # Export compressed image file
        source.to_file(output_file_path)
        print('File exported to {0}'.format(output_file_path))
        return True

def optimize_all_images_in_directory(input_directory, output_directory):
    # Create 'tinify' subfolder inside the output directory
    tinify_directory = os.path.join(output_directory, 'tinify')
    os.makedirs(tinify_directory, exist_ok=True)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_directory):
        # Check if the file is an image file
        if filename.endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp')):
            # Construct the full input path
            input_image_path = os.path.join(input_directory, filename)
            # Construct the full output path inside the 'tinify' subfolder
            output_image_path = os.path.join(tinify_directory, filename)
            # Optimize the image
            compress_image(input_image_path, output_image_path)

def select_directory_and_optimize():
    directory = filedialog.askdirectory()  # show an "Open" dialog box and return the path to the selected directory
    if directory:
        output_directory = os.path.join(directory, 'output')
        os.makedirs(output_directory, exist_ok=True)
        optimize_all_images_in_directory(directory, output_directory)
        messagebox.showinfo("Success", "Images optimized and saved in the 'output/tinify' folder.")
        refresh_file_list(directory)
    else:
        messagebox.showerror("Error", "No directory selected.")



#==================================================================
#                   Convert_images_to_webp
#==================================================================
import os
import subprocess
from glob import glob
from PIL import Image


def validate_quality_input(new_value):
    """Validates the input in the quality Entry widget."""
    if new_value.isdigit():
        if int(new_value) < 1:
            return False
        elif int(new_value) > 100:
            return False
        else:
            return True
    elif new_value == "":
        return True
    else:
        return False
    
# Create the quality label
quality_label = tk.Label(root, text="Quality:")
quality_label.grid(row=3, column=0, padx=10, pady=10)

# Create the quality Entry widget
quality_var = tk.StringVar()
quality_entry = tk.Entry(root, textvariable=quality_var, validate="key", validatecommand=(root.register(validate_quality_input), '%P'))
quality_entry.grid(row=3, column=1, padx=10, pady=10, sticky='w')

def convert_images_to_webp(image_dir):
    """Converts all JPEG and PNG images in a directory to WebP format."""
    # Get the quality value from the quality Entry widget
    # quality_value = quality_var.get()

    # # Validate the quality value
    # if not validate_quality_input(quality_value):
    #     messagebox.showerror("Error", "Invalid quality value.")
    #     return

    """Converts all JPEG and PNG images in a directory to WebP format."""
    # Iterate through each file in the directory
    for file_name in os.listdir(image_dir):
        # Get the full path of the file
        file_path = os.path.join(image_dir, file_name)
        # Check if the file is a JPEG or PNG image
        if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Open the image file using PIL
            with Image.open(file_path) as im:
                # Get the file size in kilobytes
                file_size = os.path.getsize(file_path) / 1024
                # Assign the quality value based on the file size
                if file_size >= 1000 and file_size <= 2500:
                    quality = 30
                elif file_size > 2500:
                    quality = 10
                elif file_size >= 500 and file_size < 1000:
                    quality = 60
                else:
                    # Use the default quality value of 90
                    quality = 90
    
    # Create the output directory for the WebP images
    output_dir = os.path.join(image_dir, 'webp_images')
    os.makedirs(output_dir, exist_ok=True)

    # Get a list of all JPEG and PNG images in the image directory
    img_list = []
    for img_name in glob(os.path.join(image_dir, '*.[jJ][pP][gG]')) + glob(os.path.join(image_dir, '*.[pP][nN][gG]')):
        img_list.append(img_name)

    # Convert each image to WebP format
    for img_name in img_list:
        # Create the input and output file paths
        input_path = img_name
        output_path = os.path.join(output_dir, os.path.splitext(os.path.basename(img_name))[0] + '.webp')

        # Run the cwebp executable with the input and output file paths and quality setting
        cmd = ['cwebp', input_path, '-q', str(float(quality)), '-o', output_path]
        subprocess.run(cmd)

def optimize_button_clicked():
    """Called when the Optimize button is clicked."""
    # Ask the user to select a directory containing images
    image_dir = directory

    # Refresh the file list in the listbox
    refresh_file_list(image_dir)

    # Convert the images to WebP format
    convert_images_to_webp(image_dir)

# Create the Optimize button
optimize_button = tk.Button(root, text="Optimize To Webp", command=optimize_button_clicked)
optimize_button.grid(row=3, column=1, pady=10)






# Run the Tkinter event loop
root.mainloop()
