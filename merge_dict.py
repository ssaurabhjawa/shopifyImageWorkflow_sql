from product_level_dict_v5 import product_level_dictionary
from get_product_info import get_product_info_list
import os
from ShopifyImageWorkflow_v5 import output_folder_path

def process_image():
    image_list = []
    image_dict = []
    for filename in os.listdir(output_folder_path):
        if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
            product_specs = get_product_info_list(filename)
                        file_info = extract_file_info_v5(filename)
            image_position = file_info["image_position_var"]
            if image_position == 1:
                image_list.append(product_level_dictionary(filename, output_folder_path))
            