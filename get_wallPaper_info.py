from extract_file_info_v5 import extract_file_info_v5
import os

wallpaper_sizes = [
    {"size": "60x120cm", "ratio": 0.5, "price": 60.8},
    {"size": "60x250cm", "ratio": 0.24, "price": 135.0},
    {"size": "60x305cm", "ratio": 0.20, "price": 164.7},
    {"size": "120x250cm", "ratio": 0.48, "price": 270.0},
    {"size": "120x305cm", "ratio": 0.39, "price": 329.40},
    {"size": "Wallpaper Installation", "price": 500}
]

def get_wallpaper_info_list(image_filename, image_url_list):
    # Extract image information from filename
    file_info = extract_file_info_v5(image_filename)

    # Transform the wallpaper_sizes into a list of dictionaries
    product_info_list = []
    for i, size_data in enumerate(wallpaper_sizes):

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

def wallpaper_level_dictionary(image_filename, output_folder_path, product_info_list):
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
        "Type": product_type,
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
    for product_key, product_info in google_products.items():
        if product_type == product_key:
            image_dict["Product Category"] = product_info["Product Category"]
            image_dict["Google Shopping / Google Product Category"] = product_info["Google Shopping / Google Product Category"]
            image_dict["Google Shopping / AdWords Grouping"] = product_info["Google Shopping / AdWords Grouping"]
            image_dict["Google Shopping / AdWords Labels"] = product_info["Google Shopping / AdWords Labels"]
            break

    return image_dict


#==================================================================




















