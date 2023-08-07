import os
from extract_file_info_v5 import extract_file_info_v5
from upload_to_Cloudinary import upload_to_cloudinary, get_image_url_from_cloudinary

def create_image_url_list(output_folder_path):
    image_url_list = []
    
    for filename in os.listdir(output_folder_path):
        if filename.endswith('.jpg'):
            file_path = os.path.join(output_folder_path, filename)
            file_info = extract_file_info_v5(file_path)
            
            if file_info is not None:
                handle = file_info["handle"]
                image_position = int(file_info["image_position_var"])
                variant_sku = f"{image_position}-{handle}"
                
                public_id = upload_to_cloudinary(file_path)
                image_url = get_image_url_from_cloudinary(public_id)
                
                image_url_list.append({"Variant SKU": variant_sku, "Image URL": image_url})
    
    return image_url_list

