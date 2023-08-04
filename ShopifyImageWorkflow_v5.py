import os
import csv
import tkinter as tk
from tkinter import filedialog, ttk, Listbox, Canvas, NW, END, messagebox
from PIL import Image, ImageTk
import csv
import shutil
from PIL import Image
import uuid
import tkinter.simpledialog
from dotenv import load_dotenv
from pricing_dict import artist_royalty_dict
Image.MAX_IMAGE_PIXELS = 1000000000  # Set the maximum image size limit


# Initialize tkinter app
root = tk.Tk()
root.title(" OBL Image Naming App")

# Define global variables
image_folder = ""
completed_renaming = []
renamed_files = []

# Create a frame with a border
frame = tk.Frame(root, borderwidth=2, relief="groove")
frame.grid(row=0, column=0, rowspan=4, columnspan=3)

# Configure rows and columns with grid_columnconfigure and grid_rowconfigure
for i in range(8):
    root.grid_columnconfigure(i, weight=1, minsize=50)
    root.grid_rowconfigure(i, weight=1, minsize=50)

# Create widgets with grid
for i in range(11):
    for j in range(4):
        label = tk.Label(root, text=f"({i}, {j})", borderwidth=1, relief="solid")
        label.grid(row=i, column=j, padx=1, pady=1, sticky="nsew")

def select_folder():
    global image_folder, image_files
    image_folder = filedialog.askdirectory()
    image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.gif') or f.endswith('.bmp') or f.endswith('.webp')]
    # Display list of image files in listbox
    for image in image_files:
        image_listbox.insert(tk.END, image)


count_label = tk.Label(root, text="")
count_label.grid(row=0, column=0, padx=5, pady=10, sticky="sw") 

# Create button to select folder
select_folder_button = tk.Button(root, text="Select Image Folder", command=select_folder)
select_folder_button.grid(row=1, column=1, padx=5, pady=5, sticky='sw')

# Create new Listbox widget to hold current selection
current_selection_listbox = tk.Listbox(root, height=1, width=100)
current_selection_listbox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

#==================================================================
#                           Listbox
#==================================================================

# Create listbox to display image files
image_listbox = tk.Listbox(root,width=100,height=20)
image_listbox.grid(row=0, column=1, padx=5, pady=1)

# Create Canvas to display image
image_canvas = tk.Canvas(root, width=400, height=400)
image_canvas.grid(row=0, column=2, padx=5, pady=1, sticky="w")

# Function to display selected image
def show_image(event):
    # Get selected file name
    selected_file = current_selection_listbox.get(current_selection_listbox.curselection())

    # Load and display image on canvas
    img = Image.open(os.path.join(image_folder, selected_file))
    img.thumbnail((400, 400))
    img_tk = ImageTk.PhotoImage(img)
    image_canvas.create_image(0, 0, anchor=NW, image=img_tk)
    image_canvas.image = img_tk

# Bind Listbox selection event to show_image function
image_listbox.bind('<<ListboxSelect>>', show_image)

# Define input variables
product_type_options = ["canvas", "acrylic", "wallpaper", "poster", "notebook", "pre-sketchbook", "greetingcard", "mugs", "stickers","homepageimages"]
product_type_var = tk.StringVar(root, product_type_options[0])

#==================================================================
#                          Refresh Listbox
#==================================================================
def refresh_images():
    # Clear current image selection
    current_selection_listbox.selection_clear(0, END)

    # Clear current image on canvas
    image_canvas.delete("all")

    # Get list of image files in image folder
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]

    # Clear current listbox options
    image_listbox.delete(0, END)

    # Add image files to listbox options
    for f in image_files:
        image_listbox.insert(END, f)

    # Bind Listbox selection event to show_image function
    image_listbox.bind('<<ListboxSelect>>', show_image)


refresh_button = tk.Button(root, text="Refresh", width = 15, command=refresh_images)
refresh_button.grid(row=1, column=1, padx=5, pady=5, sticky='se')

#==================================================================
#                       Segrage Images by Ratio
#==================================================================

# refresh_button = tk.Button(root, text="Segregate Images", width = 15, command=segregate_images_by_aspect_ratio)
# refresh_button.grid(row=1, column=1, padx=5, pady=5, sticky='s')



#==================================================================
#                           Artist Dropdown
#==================================================================

artist_label = tk.Label(root, text="Artist:")
artist_label.grid(row=4, column=1, padx=5, pady=5,sticky='n')
# Create the dropdown menu
selected_artist = tk.StringVar(root, value=list(artist_royalty_dict.keys())[0])
artist_dropdown = ttk.Combobox(root, textvariable=selected_artist, values=list(artist_royalty_dict.keys()))

# Configure the dropdown menu
artist_dropdown.config(state="readonly", width=15)
# Display the dropdown menu using grid
artist_dropdown.grid(row=4, column=1,padx=5, pady=5, sticky='s')

#==================================================================
#                           Product Type Dropdown
#==================================================================

# Create the label and dropdown for the product type dropdown
product_type_label = tk.Label(root,  text="Product Type:")
product_type_dropdown = ttk.Combobox(root, textvariable=product_type_var, values=product_type_options)
product_type_dropdown.config(width=15)

product_type_label.grid(row=4, column=1, padx=5, pady=5, sticky="nw")
product_type_dropdown.grid(row=4, column=1, padx=5, pady=5, sticky="sw")

root.rowconfigure(3, minsize=70)

title_var = tk.StringVar(root)
# Create variable for image position
image_position_var = tk.IntVar(value=0)

title_label = tk.Label(root, width=10, text="Title:")
title_entry = tk.Entry(root, textvariable=title_var, width=100)
title_label.grid(row=3, column=0, padx=5, pady=1, sticky="e")
title_entry.grid(row=3, column=1, padx=5, pady=1)


# Create the renamed_listbox
renamed_listbox = tk.Listbox(root, width=100)
renamed_listbox.grid(row=6, column=1, padx=10, pady=10)

#==================================================================
#                           OUTPUT Folder
#==================================================================
def display_output_folder_path():
    global output_folder_path
    if output_folder_path:      
        # Create label widget to display output folder path
        output_path_label = tk.Label(root, text=output_folder_path)

        # Display output folder path label widget in grid
        output_path_label.grid(row=4, column=3, padx=5, pady=1)
    else:
        messagebox.showerror("Error", "The output folder path has not been set.")



from tkinter import messagebox
def create_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory(title="Select output folder")
    if output_folder_path:
        os.makedirs(output_folder_path, exist_ok=True)
        messagebox.showinfo("Success", f"Output folder created at {output_folder_path}")
        # Display list of image files in output_listbox
        output_files = [f for f in os.listdir(output_folder_path) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.webp')]        
        output_listbox.delete(0, tk.END)
        display_output_folder_path()
        for file in output_files:
            output_listbox.insert(tk.END, file)
    else:
        messagebox.showerror("Error", "No output folder selected")

# Create Output Folder button
create_output_folder_button = tk.Button(root, text="Select Output Folder", command=create_output_folder)
create_output_folder_button.grid(row=7, column=1, padx=10, pady=10)


#==================================================================
#                           Name Creation
#==================================================================
def rename_file():
    # Activate current_selection_listbox
    current_selection_listbox.focus_set()


    # Get selected image filename
    selected_file = current_selection_listbox.get(current_selection_listbox.curselection())

    if not selected_file:
        messagebox.showerror("Error", "Please select an image to rename.")
        return

    # Get image aspect ratio
    img_path = os.path.join(image_folder, selected_file)
    with Image.open(img_path) as img:
        width, height = img.size
        aspect_ratio = round(width / height, 2)
        

    # Get file extension
    ext = os.path.splitext(selected_file)[1]

    # Create new filename with aspect ratio and UUID
    new_filename = f"{aspect_ratio}--{uuid.uuid4().hex[:6]}--{product_type_var.get()}--{title_var.get()}--{image_position_var.get()}--{selected_artist.get()}{ext}"

    try:
        # Check if file exists in the old file path
        if os.path.isfile(img_path):
            # Copy file to output folder
            shutil.copy(img_path, os.path.join(output_folder_path, new_filename))

            # Update current_selection_listbox
            current_selection_listbox.delete(0, tk.END)
            current_selection_listbox.insert(0, new_filename)

            # Clear current_selection_listbox
            current_selection_listbox.selection_clear(0, tk.END)

            # Update image_listbox
            image_listbox.delete(0, tk.END)
            for file in os.listdir(image_folder):
                if file.endswith((".jpg", ".jpeg", ".png", ".webp")):
                    image_listbox.insert(tk.END, file)

            # Add new filename to renamed_files array
            renamed_files.append(new_filename)

            # Update renamed_listbox
            renamed_listbox.delete(0, END)
            for file in renamed_files:
                renamed_listbox.insert(END, file)
        else:
            messagebox.showerror("Error", "The selected file no longer exists.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while renaming the file: {e}")
        # Print error message to console for debugging
        print(f"Error occurred while renaming the file: {str(e)}")


#==================================================================
#                           Display Image
#==================================================================



def update_current_selection(event):
    # Get selected file name
    selected_file = image_listbox.get(image_listbox.curselection())

    # Update current selection Listbox
    current_selection_listbox.delete(0, tk.END)
    current_selection_listbox.insert(0, selected_file)

# Bind the image_listbox to update the current_selection_listbox
image_listbox.bind('<Double-Button-1>', update_current_selection)

# Bind the current_selection_listbox to rename_file function
current_selection_listbox.bind('<<ListboxSelect>>', rename_file)

# "Rename File" and binds it to the function 'rename_file'.
rename_button = tk.Button(root, text="<--Rename Me", command=rename_file)
rename_button.grid(row=2, column=2, padx=5, pady=1, sticky="w")

# Listbox widget to display the output image files and set its width
output_listbox = tk.Listbox(root, width=70,height=20)
output_listbox.grid(row=0, column=3, padx=5, pady=1)


#==================================================================
#           Populate Title Field with Double Click & Rename    
#==================================================================
# Create the Rename File Text Box
renameFileTextBox = tk.Entry(root, width=100)
renameFileTextBox.grid(row=5, column=1, padx=5, pady=1)

def select_file(event):
    selected_file = output_listbox.get(output_listbox.curselection())
    renameFileTextBox.delete(0, tk.END)
    renameFileTextBox.insert(tk.END, selected_file)

output_listbox.bind('<Double-Button-1>', select_file)

from pathlib import Path

def rename_file_from_text():
    # Activate current_selection_listbox
    current_selection_listbox.focus_set()

    # Get selected image filename
    selected_file = current_selection_listbox.get(current_selection_listbox.curselection())

    if not selected_file:
        messagebox.showerror("Error", "Please select an image to rename.")
        return
    
    old_path = Path(image_folder) / selected_file

    # Get the new file name from renameFileTextBox
    new_file_name = renameFileTextBox.get()
    new_path = Path(output_folder_path) / new_file_name

    try:
        # Rename the file
        old_path.rename(new_path)

        # Update current_selection_listbox
        current_selection_listbox.delete(0, tk.END)
        current_selection_listbox.insert(0, new_file_name)

        # Clear current_selection_listbox
        current_selection_listbox.selection_clear(0, tk.END)

        # Update image_listbox
        image_listbox.delete(0, tk.END)
        for file in os.listdir(image_folder):
            if file.endswith((".jpg", ".jpeg", ".png", ".webp")):
                image_listbox.insert(tk.END, file)

        # Add new filename to renamed_files array
        renamed_files.append(new_file_name)

        # Update renamed_listbox
        renamed_listbox.delete(0, END)
        for file in renamed_files:
            renamed_listbox.insert(END, file)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while renaming the file: {e}")


# Create the Rename Button
renameButton = tk.Button(root, text="<--rename_file_from_text", command=rename_file_from_text)
renameButton.grid(row=5, column=2, padx=5, pady=5, sticky="w")

#==================================================================
#                           Update Output Listbox
#==================================================================

# Define function to update the output listbox
def update_output_listbox():
    output_listbox.delete(0, tk.END)
    for file in os.listdir(output_folder_path):
        if file.endswith((".jpg", ".jpeg", ".png", ".webp")):
            output_listbox.insert(tk.END, file)

# Create button to update the output listbox
update_output_button = tk.Button(root, width=25,text="Update Output Listbox", command=update_output_listbox)
update_output_button.grid(row=1, column=3, padx=5, pady=5, sticky="s")






#==================================================================
#                          Update Image Position
#==================================================================

# Create the Listbox widget (outbox_listbox)
outbox_listbox = tk.Listbox(root,height=10, width=100)
outbox_listbox.grid(row=6, column=3, padx=5, pady=1)

def select_folder_for_renaming():
    global folder_path_renaming, image_files
    folder_path_renaming = filedialog.askdirectory()
    image_files = [f for f in os.listdir(folder_path_renaming) if f.endswith('.jpg') or f.endswith('.jpeg') or f.endswith('.png') or f.endswith('.webp')]
    # Display list of image files in listbox
    for image in image_files:
        outbox_listbox.insert(tk.END, image)


# Create button to select folder
select_folder_forRename_button = tk.Button(root, text="Select Image Folder", command=select_folder_for_renaming)
select_folder_forRename_button.grid(row=8, column=3, padx=5, pady=5, sticky='w')


def update_image_position():
    global folder_path_renaming

    # Ask user to select a folder
    folder_path_renaming = filedialog.askdirectory(title="Select a folder")

    # Ask user for image position number to rename
    image_position = tk.simpledialog.askinteger("Image Position", "Enter the image position number to rename:", minvalue=1)

    if not folder_path_renaming:
        messagebox.showerror("Error", "Please select a folder.")
        return

    if not image_position:
        messagebox.showerror("Error", "Please enter the image position number to rename.")
        return
    
    # Iterate through each file in the folder and rename it with updated image position number
    for file in os.listdir(folder_path_renaming):
        if file.endswith((".jpg", ".jpeg", ".png", ".webp")):
            # Remove extension from filename
            filename_without_ext = os.path.splitext(file)[0]
            # Get aspect ratio, uuid, product type, title, and artist from the filename
            filename_parts = filename_without_ext.split("--")
            aspect_ratio = filename_parts[0]
            uuid = filename_parts[1]
            product_type = filename_parts[2]
            title = (filename_parts[3])
            artist_name = filename_parts[5] # assuming artist name is separated by underscore

            # Create new filename with updated image position number and artist name
            ext = os.path.splitext(file)[1]
            new_filename = f"{aspect_ratio}--{uuid}--{product_type}--{title}--{image_position}--{artist_name}{ext}"

            # Rename file
            os.rename(os.path.join(folder_path_renaming, file), os.path.join(output_folder_path, new_filename))


    # Update file_listbox
    for file in os.listdir(folder_path_renaming):
        outbox_listbox.insert(tk.END, file)
    
    tk.messagebox.showinfo("Success", f"All files in {folder_path_renaming} have been renamed with image position {image_position}.")

def refresh_renamed_images():
    # Clear current image selection
    current_selection_listbox.selection_clear(0, END)

    # Get list of image files in image folder
    image_files = [f for f in os.listdir(folder_path_renaming) if os.path.isfile(os.path.join(folder_path_renaming, f))]

    # Clear current listbox options
    outbox_listbox.delete(0, END)

    # Add image files to listbox options
    for f in image_files:
        outbox_listbox.insert(END, f)



refresh_button = tk.Button(root, text="Refresh", width = 15, command=refresh_renamed_images)
refresh_button.grid(row=8, column=3, padx=5, pady=5)

# Create the "Update Image Position" button
update_position_button = tk.Button(root, text="Update Image Position", command=update_image_position)
update_position_button.grid(row=8, column=3, padx=5, pady=5, sticky="e")


#==================================================================
#      move_images_to_new_location
#==================================================================
from move_image_to_new_location import move_images_to_new_location

# Create button to move images to new location
move_button = tk.Button(root, text="Move Images", command=lambda: move_images_to_new_location())

# Display button in grid
move_button.grid(row=8, column=2, padx=5, pady=5, sticky="w")




#==================================================================
#      Step 2. Process Directory
#==================================================================
from datetime import datetime
import os
import csv
import pathlib
from datetime import datetime
import time


def write_csv(images_list):
    fieldnames = ['Handle', 'Title', 'Body (HTML)', 'Vendor', 'Product Category', 'Type', 'Tags', 'Published', 'Option1 Name', 'Option1 Value', 'Option2 Name', 'Option2 Value', 'Option3 Name', 'Option3 Value', 'Variant SKU', 'Variant Grams', 'Variant Inventory Tracker', 'Variant Inventory Qty', 'Variant Inventory Policy', 'Variant Fulfillment Service', 'Variant Price', 'Variant Compare At Price', 'Variant Requires Shipping', 'Variant Taxable', 'Variant Barcode', 'Image Src', 'Image Position', 'Image Alt Text', 'Gift Card', 'SEO Title', 'SEO Description', 'Google Shopping / Google Product Category', 'Google Shopping / Gender', 'Google Shopping / Age Group', 'Google Shopping / MPN', 'Google Shopping / AdWords Grouping', 'Google Shopping / AdWords Labels', 'Google Shopping / Condition', 'Google Shopping / Custom Product', 'Google Shopping / Custom Label 0', 'Google Shopping / Custom Label 1', 'Google Shopping / Custom Label 2', 'Google Shopping / Custom Label 3', 'Google Shopping / Custom Label 4', 'Variant Image', 'Variant Weight Unit', 'Variant Tax Code', 'Cost per item', 'Included / United Arab Emirates', 'Included / International', 'Price / International', 'Compare At Price / International', 'Status']
    # Create directory for CSV file
    csv_dir = os.path.join(output_folder_path, 'product_csv')
    pathlib.Path(csv_dir).mkdir(parents=True, exist_ok=True)
    
    # Create filename with current timestamp
    current_time = datetime.now().strftime("%H_%M_%S")
    csv_filename = f"products_{current_time}.csv"
    csv_path = os.path.join(csv_dir, csv_filename)

    
    with open(csv_path, "w", newline="", encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for image_dict in images_list:
            writer.writerow(image_dict)
            
    messagebox.showinfo("CSV Generated", "CSV file generated successfully!")

from product_level_dict_v5 import product_level_dictionary
from variant_level_dict import variant_level_dictionary
from get_product_info import get_product_info_list
from extract_file_info_v5 import extract_file_info_v5

def count_files_by_handle(output_folder_path):
    handle_dict = {}
    for filename in os.listdir(output_folder_path):
        file_path = os.path.join(output_folder_path, filename)
        file_info = extract_file_info_v5(file_path)

        # Check if file_info is not None before proceeding
        if file_info is not None:
            handle = file_info["handle"]
            if handle in handle_dict:
                handle_dict[handle] += 1
            else:
                handle_dict[handle] = 1

    return handle_dict


import itertools

def process_image(output_folder_path):
    def sort_sku(variant):
        # Split the SKU into numeric and non-numeric parts
        parts = variant.get("Variant SKU", "").split("-")
        numeric_part = int(parts[0]) if parts and parts[0].isdigit() else 0
        return numeric_part

    image_list = []
    handle_dict = count_files_by_handle(output_folder_path)

    for filename in os.listdir(output_folder_path):
        file_path = os.path.join(output_folder_path, filename)
        file_info = extract_file_info_v5(file_path)

        # Check if file_info is not None before proceeding
        if file_info is not None:
            handle = file_info["handle"]
            image_position = int(file_info["image_position_var"])
            product_info_list = get_product_info_list(file_path)
            
            if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
                if image_position == 1:
                    product_info_list_1 = product_info_list[0]
                    image_list.append(product_level_dictionary(filename, output_folder_path, product_info_list_1))
                    image_list.extend(product_info_list[handle_dict[handle]:])
                elif image_position == 2:
                    product_info_list_2 = product_info_list[1]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_2))
                elif image_position == 3:
                    product_info_list_3 = product_info_list[2]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_3))
                elif image_position == 4:
                    product_info_list_4 = product_info_list[3]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_4))

    # Sort image_list by Variant SKU first
    image_list.sort(key=sort_sku)

    # Group image_list by handle
    grouped_image_list = []
    for handle, variants in itertools.groupby(image_list, key=lambda x: x.get("handle")):
        grouped_image_list.extend(sorted(variants, key=sort_sku))

    return grouped_image_list
  


def process_images():
    images_list = process_image(output_folder_path)
    write_csv(images_list)



    



process_button = tk.Button(root, text="Process Images", command=process_images)
process_button.grid(row=8, column=2, padx=10, pady=10, sticky='e')





# Run the main event loop
root.mainloop()

# Destroy the GUI window and exit the application
root.destroy()
