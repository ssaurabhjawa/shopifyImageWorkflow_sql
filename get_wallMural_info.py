from extract_file_info_v5 import extract_file_info_v5
import os

wall_mural_sizes = [
    {"size": "2.4 meters x 2.4 meters", "price": 738.4},
    {"size": "2.7 meters x 3 meters", "price": 949},
    {"size": "2.4 meters x 4.5 meters", "price": 1192},
    {"size": "2.7 meters x 5 meters", "price": 1435},
    {"size": "2.4 meters x 6 meters", "price": 1516},
    {"size": "2.7 meters x 4 meters", "price": 1192},
    {"size": "2.4 meters x 3.5 meters", "price": 976},
    {"size": "2.7 meters x 6 meters", "price": 1678},
    {"size": "2.4 meters x 2 meters", "price": 652},
    {"size": "2.7 meters x 4.5 meters", "price": 1313.5},
    {"size": "Wallpaper Installation", "price": 500}
]


def get_wallmural_info_list(image_filename, image_url_list):
    # Extract image information from filename
    file_info = extract_file_info_v5(image_filename)

    # Transform the wallpaper_sizes into a list of dictionaries
    product_info_list = []
    for i, size_data in enumerate(wall_mural_sizes):
        variant_sku = f"{i + 1}-{file_info['handle']}"
        
        # Find the dictionary with matching "Variant SKU" in the image_url_list
        matching_dict = next((item for item in image_url_list if item["Variant SKU"] == variant_sku), None)

        product_info = {
            "Handle": file_info["handle"],
            "Option1 Value": size_data["size"],   # Material
            "Variant Price": size_data["price"],    # Price
            "Variant Inventory Policy": "deny",
            "Variant Fulfillment Service": "manual",
            "Variant SKU": variant_sku,
            "Variant Inventory Qty": 10,
            "Variant Image": matching_dict["Image URL"] if matching_dict else ""  # Get the image URL from the matching_dict
        }
        product_info_list.append(product_info)

    return product_info_list


from upload_to_Cloudinary import upload_to_cloudinary, get_image_url_from_cloudinary

google_products = {
    "wallpaper": {
        "Product Category": "Home & Garden > Decor > Wallpaper",
        "Google Shopping / Google Product Category": "2334",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Wallpaper",
        "Google Shopping / AdWords Labels": "HomeGarden, Decor"
    },
    # Add other product types and their information if needed
}

#==================================================================
#              Product_level_dictionary
#==================================================================

def wallmural_level_dictionary(image_filename, output_folder_path, product_info_list):
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

    image_dict = {
        "Handle":uuid ,
        "Title": title,
        "Body (HTML)": "",
        "Vendor": artist,
        "Product Category": "",
        "Type": "Wall Mural",
        "Tags": "Miscellaneous",
        "Published": "TRUE",
        "Option1 Name": "Sizes",
        "Option1 Value": product_info_list["Option1 Value"],
        "Option2 Name": "",
        "Option2 Value":"",
        "Option3 Name":"",
        "Option3 Value": "",
        "Variant SKU" : str(image_position) + "-" + uuid,
        "Variant Inventory Qty":10,
        "Variant Inventory Policy": "deny",
        "Variant Fulfillment Service":"manual",
        "Variant Price":product_info_list["Variant Price"],
        "Image Src": get_image_url_from_cloudinary(public_id),  # Use the Cloudinary URL
        "Image Alt Text": title,
        "Gift Card": "FALSE",
        "SEO Title": title,
        "SEO Description": "",
        "Google Shopping / Google Product Category": "",
        "Google Shopping / AdWords Grouping": "",
        "Google Shopping / AdWords Labels": "",
        "Google Shopping / Condition": "new",
        "Variant Image": get_image_url_from_cloudinary(public_id),
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
    for product_key, product_info in google_products.items():
        if product_type == product_key:
            image_dict["Product Category"] = product_info["Product Category"]
            image_dict["Google Shopping / Google Product Category"] = product_info["Google Shopping / Google Product Category"]
            image_dict["Google Shopping / AdWords Grouping"] = product_info["Google Shopping / AdWords Grouping"]
            image_dict["Google Shopping / AdWords Labels"] = product_info["Google Shopping / AdWords Labels"]
            break

    return image_dict


#==================================================================




















