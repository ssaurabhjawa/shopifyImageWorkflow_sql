from upload_to_Cloudinary import upload_to_cloudinary, get_image_url_from_cloudinary
from extract_file_info_v5 import extract_file_info_v5
import os
from get_product_info import get_product_info_list



#==================================================================
#              Product_level_dictionary
#==================================================================

def variant_level_dictionary(image_filename, output_folder_path, product_info_list_1):
    file_path = os.path.join(output_folder_path, image_filename)
    public_id = upload_to_cloudinary(file_path)
    # Extract image information from filename
    file_info = extract_file_info_v5(image_filename)
    aspect_ratio = file_info["aspect_ratio"]
    uuid = file_info["handle"]
    product_type = file_info["product_material"]
    title = file_info["title"]
    image_position = file_info["image_position_var"]
    artist= file_info["vendor"]
    # Create a dictionary for the image with all the CSV fields
    image_dict = {
        "Handle":uuid ,
        "Title": title,
        "Body (HTML)": "",
        "Vendor": artist,
        "Product Category": "",
        "Type": product_type,
        "Tags": "Miscellaneous",
        "Published": "TRUE",
        "Option1 Name": "Material",
        "Option1 Value": product_info_list_1["Option1 Value"],
        "Option2 Name": "Frame",
        "Option2 Value":product_info_list_1["Option2 Value"],
        "Option3 Name":"Size",
        "Option3 Value": product_info_list_1["Option3 Value"],
        "Variant Inventory Qty":10,
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service":"manual",
        "Variant Price":product_info_list_1["Variant Price"],
        "Image Src": get_image_url_from_cloudinary(public_id),  # Use the Cloudinary URL
        "Image Alt Text": title,
        "Gift Card": "FALSE",
        "SEO Title": title,
        "SEO Description": "",
        "Google Shopping / Google Product Category": "",
        "Google Shopping / AdWords Grouping": "",
        "Google Shopping / AdWords Labels": "",
        "Google Shopping / Condition": "new",
        "Variant Image": "",
        "Variant Weight Unit": "kg",
        "Variant Tax Code": "",
        "Cost per item": "",
        "Included / United Arab Emirates": "TRUE",
        "Included / International": "FALSE",
        "Price / International": "",
        "Compare At Price / International": "",
        "Status": "active",
        "Image Position": image_position,
    }

        # Fill in the Google Shopping fields based on the product type
    for product in google_products:
        if product_type == product["Product"]:
            image_dict["Product Category"] = product["Product Category"]
            image_dict["Google Shopping / Google Product Category"] = product["Google Shopping / Google Product Category"]
            image_dict["Google Shopping / AdWords Grouping"] = product["Google Shopping / AdWords Grouping"]
            image_dict["Google Shopping / AdWords Labels"] = product["Google Shopping / AdWords Labels"]
            break

    return image_dict

# product_level_dictionary("0.8--1a6d85--Canvas--City in Purple Sunset--1--OBL Display SS.jpg", "D:/OBLDisplay/Completed_products_1/images - Pinga")