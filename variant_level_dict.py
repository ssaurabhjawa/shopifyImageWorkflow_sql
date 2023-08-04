import os
import uuid
from dotenv import load_dotenv
from pricing_dict import artist_royalty_dict
import cloudinary
import cloudinary.uploader
import cloudinary.api
from extract_file_info_v5 import extract_file_info_v5
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from upload_to_Cloudinary import upload_to_cloudinary, get_image_url_from_cloudinary

#==================================================================
#                    Variant_level_dictionary 
#==================================================================
def variant_level_dictionary(image_filename, output_folder_path,product_info_list):
    file_path = os.path.join(output_folder_path, image_filename)
    public_id = upload_to_cloudinary(file_path)
    # Extract image information from filename
    file_info = extract_file_info_v5(image_filename)
    aspect_ratio = file_info["aspect_ratio"]
    uuid = file_info["handle"]
    product_type = file_info["product_material"]
    title = file_info["title"]
    image_position = file_info["image_position_var"]

    # Create a dictionary for the image with all the CSV fields
    image_dict = {
        "Handle":uuid ,
        "Image Src": get_image_url_from_cloudinary(public_id),  # Use the Cloudinary URL
        "Image Alt Text": title,
        "Image Position": image_position,
        "Handle": file_info["handle"],
        "Option1 Value": product_info_list["Option1 Value"],   # Material
        "Option2 Value": product_info_list["Option2 Value"],   # Frame Type
        "Option3 Value": product_info_list["Option3 Value"],   # Size
        "Variant SKU" : str(image_position) + "-" + uuid,
        "Variant Inventory Qty":10,
        "Variant Price": product_info_list["Variant Price"],    
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service":"manual",
}
    return image_dict

