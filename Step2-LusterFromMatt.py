import os
import shutil
from extract_file_info_v5 import extract_file_info_v5

# dest_dir = r"C:\Users\Saurabh\Documents\OneBigLoveProducts\Products"


new_image_position = [49, 53, 57, 61, 65, 69, 73]

frame_positions_list = [
    {"old_position": 21, "new_position": 49},
    {"old_position": 25, "new_position": 53},
    {"old_position": 29, "new_position": 57},
    {"old_position": 33, "new_position": 61},
    {"old_position": 37, "new_position": 65},
    {"old_position": 41, "new_position": 69},
    {"old_position": 45, "new_position": 73}
]

def main():
    dest_dir = r"D:\OBLJJAWA\My Drive\Designers\SwetaWork\Product_Sweta_completed"
    # dest_dir = r"C:\Users\Saurabh\Documents\OneBigLoveProducts\Products"
    # dest_dir = r"D:\OBLJJAWA\My Drive\Products"

    frame_positions_list = [
        (21, 49),
        (25, 53),
        (29, 57),
        (33, 61),
        (37, 65),
        (41, 69),
        (45, 73)
    ]
  
    for subfolder_name in os.listdir(dest_dir):
        subfolder_path = os.path.join(dest_dir, subfolder_name)
        if os.path.isdir(subfolder_path):
            existing_positions = []
            for filename in os.listdir(subfolder_path):
                if filename.lower() == "desktop.ini":
                    continue  # Skip processing desktop.ini
                file_path = os.path.join(subfolder_path, filename)
                file_info = extract_file_info_v5(file_path)
                if file_info:
                    image_position = file_info["image_position_var"]
                    if image_position in [pos[0] for pos in frame_positions_list]:
                        index = [pos[0] for pos in frame_positions_list].index(image_position)
                        new_image_position = frame_positions_list[index][1]
                        
                        # Split file name into parts based on delimiter
                        file_parts = filename.split("--")
                        if len(file_parts) >= 5:
                            file_parts[4] = str(new_image_position)
                            new_filename = "--".join(file_parts)
                            
                            new_subfolder_path = os.path.join(dest_dir, subfolder_name)
                            os.makedirs(new_subfolder_path, exist_ok=True)
                            
                            new_file_path = os.path.join(new_subfolder_path, new_filename)
                            shutil.copy(file_path, new_file_path)
                            print(f"File '{filename}' copied and renamed to '{new_filename}'")

if __name__ == "__main__":
    main()

   
