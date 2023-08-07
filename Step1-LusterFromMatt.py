import os
import shutil
from extract_file_info_v5 import extract_file_info_v5

frame_positions = {
    21: 49,
    25: 53,
    29: 57,
    33: 61,
    37: 65,
    41: 69,
    45: 73
}

dest_dir = r"D:\OBLJJAWA\My Drive\Products"


new_image_position = [49, 53, 57, 61, 65, 69, 73]

def check_images_with_positions(source_dir, new_image_position):
    # Initialize a flag to check if any image position matches the ones in the new_image_position list
    any_matching_position = False

    # Iterate through all the folders in the source directory
    for foldername, subfolders, filenames in os.walk(source_dir):
        # Iterate through all the files in each folder
        for filename in filenames:
            # Extract the image position using the extract_file_info_v5 function
            file_info = extract_file_info_v5(os.path.join(foldername, filename))
            if file_info is None:
                continue
            image_position = file_info["image_position_var"]
            # Check if the image position is in the new_image_position list
            if image_position in new_image_position:
                any_matching_position = True
                break

    return any_matching_position

def copy_images_with_positions(dest_dir, frame_positions, new_image_position):
    # Check if any image position matches the ones in the new_image_position list
    any_matching_position = check_images_with_positions(dest_dir, new_image_position)


    if any_matching_position:
        print("Skipping copying files as there are images with matching image positions.")
    else:
        # Iterate through all the folders in the source directory
        for foldername, _, filenames in os.walk(dest_dir):
            # Extract the subfolder name from the current folder path
            subfolder_name = os.path.relpath(foldername, dest_dir)
            # Iterate through all the files in each folder
            for filename in filenames:
                # Extract the image position using the extract_file_info_v5 function
                file_info = extract_file_info_v5(os.path.join(foldername, filename))
                if file_info is None:
                    continue
                image_position = file_info["image_position_var"]
                # Check if the image position is in the new_image_position list
                if image_position in new_image_position:
                    continue  # Skip copying this particular file
                # Replace the image position with the corresponding value in the frame_positions dictionary
                new_image_position_value = frame_positions.get(image_position)
                if new_image_position_value is not None:
                    # Copy the image to the destination directory with the new image position in the filename
                    new_filename = filename.replace(str(image_position), str(new_image_position_value))
                    new_subfolder_path = os.path.join(dest_dir, subfolder_name)
                    os.makedirs(new_subfolder_path, exist_ok=True)  # Create the subfolder if it doesn't exist
                    shutil.copy(os.path.join(foldername, filename), os.path.join(new_subfolder_path, new_filename))
                else:
                    print(f"Warning: Image position {image_position} not found in frame_positions dictionary.")

# Call the function with the destination directory and other parameters
copy_images_with_positions(dest_dir, frame_positions, new_image_position)
