import os
import csv
import datetime
import re
from extract_file_info_v5 import extract_file_info_v5


ArtDictionary = [
    {'Material': 'Canvas', 'Frame': 'Gallery Wrap', 'Image Position': 1},
    {'Material': 'Canvas', 'Frame': 'White Floating Frame', 'Image Position': 5},
    {'Material': 'Canvas', 'Frame': 'Black Floating Frame', 'Image Position': 9},
    {'Material': 'Canvas', 'Frame': 'Golden Floating Frame', 'Image Position': 13},
    {'Material': 'Canvas', 'Frame': 'Rolled Art', 'Image Position': 17},
    {'Material': 'Matt Paper', 'Frame': 'White Frame', 'Image Position': 21},
    {'Material': 'Matt Paper', 'Frame': 'Black Frame', 'Image Position': 25},
    {'Material': 'Matt Paper', 'Frame': 'Brown Frame', 'Image Position': 29},
    {'Material': 'Matt Paper', 'Frame': 'White Frame With Mount', 'Image Position': 33},
    {'Material': 'Matt Paper', 'Frame': 'Black Frame With Mount', 'Image Position': 37},
    {'Material': 'Matt Paper', 'Frame': 'Brown Frame With Mount', 'Image Position': 41},
    {'Material': 'Matt Paper', 'Frame': 'Rolled Art', 'Image Position': 45},
    {'Material': 'Premium Luster Paper', 'Frame': 'White Frame', 'Image Position': 49},
    {'Material': 'Premium Luster Paper', 'Frame': 'Black Frame', 'Image Position': 53},
    {'Material': 'Premium Luster Paper', 'Frame': 'Brown Frame', 'Image Position': 57},
    {'Material': 'Premium Luster Paper', 'Frame': 'White Frame With Mount', 'Image Position': 61},
    {'Material': 'Premium Luster Paper', 'Frame': 'Black Frame With Mount', 'Image Position': 65},
    {'Material': 'Premium Luster Paper', 'Frame': 'Brown Frame With Mount', 'Image Position': 69},
    {'Material': 'Premium Luster Paper', 'Frame': 'Rolled Art', 'Image Position': 73}
]

dest_dir = r"D:\OBLJJAWA\My Drive\Designers\SwetaWork\Product_Sweta_completed"
# dest_dir = r"C:\Users\Saurabh\Documents\OneBigLoveProducts\Products"
# dest_dir = r"D:\OBLJJAWA\My Drive\Products"

def check_images_with_positions(source_dir, new_image_position):
    any_matching_position = False

    for foldername, _, filenames in os.walk(source_dir):
        for filename in filenames:
            file_info = extract_file_info_v5(os.path.join(foldername, filename))
            if file_info is None:
                continue
            image_position = file_info["image_position_var"]
            if image_position in new_image_position:
                any_matching_position = True
                break

    return any_matching_position


def report_complete_folders(source_dir, art_dict):
    complete_folders_report = []

    for foldername, _, _ in os.walk(source_dir):
        subfolder_name = os.path.relpath(foldername, source_dir)

        all_images_exist = all(
            check_images_with_positions(foldername, [entry["Image Position"]])
            for entry in art_dict
        )

        if all_images_exist:
            complete_entry = {
                "Subfolder": subfolder_name,
                "Status": "Complete"
            }
            complete_folders_report.append(complete_entry)

    return complete_folders_report

# Destination directory for the Reports folder
reports_dir = r'D:\OBLJJAWA\My Drive\Reports'
source_dir = dest_dir

# Create a folder with a timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
timestamp = re.sub(r'[^a-zA-Z0-9]', '', timestamp)
report_folder = os.path.join(reports_dir, f"Report_{timestamp}")
os.makedirs(report_folder, exist_ok=True)

complete_folders_report_file = os.path.join(report_folder, 'complete_folders_report.csv')

# Get the report data for complete folders
complete_folders_report_data = report_complete_folders(source_dir, ArtDictionary)

# Write the complete folders report to a CSV file inside the folder
with open(complete_folders_report_file, mode='w', newline='') as csvfile:
    fieldnames = ["Subfolder", "Status"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(complete_folders_report_data)

print(f"Complete folders report created: {complete_folders_report_file}")
