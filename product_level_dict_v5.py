from upload_to_Cloudinary import upload_to_cloudinary, get_image_url_from_cloudinary
from extract_file_info_v5 import extract_file_info_v5
import os
from get_product_info import get_product_info_list

google_products = [
    {
        "Product": "canvas",
        "Product Category": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / Google Product Category": "500044",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / AdWords Labels": "HomeGarden, Decor, Artwork, PostersPrints"
    },
    {
        "Product": "acrylic",
        "Product Category":"Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / Google Product Category": "500044",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / AdWords Labels": ""
    },
    {
        "Product": "wallpaper",
        "Product Category":"Home & Garden > Decor > Wallpaper",
        "Google Shopping / Google Product Category": "2334",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Wallpaper",
        "Google Shopping / AdWords Labels": "HomeGarden, Decor"
    },
    {
        "Product": "wallmural",
        "Product Category":"Home & Garden > Decor > Wallpaper",
        "Google Shopping / Google Product Category": "2334",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Wallpaper",
        "Google Shopping / AdWords Labels": "HomeGarden, Decor"
    },
    {
        "Product": "poster",
        "Product Category": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / Google Product Category": "500044",
        "Google Shopping / AdWords Grouping": "Home & Garden > Decor > Artwork > Posters, Prints, & Visual Artwork",
        "Google Shopping / AdWords Labels": "HomeGarden, Decor, Artwork, PostersPrints"
    },
    {
        "Product": "notebook",
        "Product Category": "Office Supplies > General Office Supplies > Paper Products > Notebooks & Notepads",
        "Google Shopping / Google Product Category": "961",
        "Google Shopping / AdWords Grouping": "Office Supplies > General Office Supplies > Notebooks & Notepads",
        "Google Shopping / AdWords Labels": ""
    },
    {
        "Product": "mugs",
        "Product Category":"Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs",
        "Google Shopping / Google Product Category": "2169",
        "Google Shopping / AdWords Grouping": "Home & Garden > Kitchen & Dining > Tableware > Drinkware > Mugs",
        "Google Shopping / AdWords Labels": ""
    },
    {
        "Product": "puzzles",
        "Product Category":"Toys & Games > Puzzles > Jigsaw Puzzle Accessories",
        "Google Shopping / Google Product Category": "3867",
        "Google Shopping / AdWords Grouping": "Toys & Games > Puzzles",
        "Google Shopping / AdWords Labels": ""
    },
    {
        "Product": "Stickers",
        "Product Category": "Arts & Entertainment > Hobbies & Creative Arts > Arts & Crafts > Art & Crafting Materials > Embellishments & Trims > Decorative Stickers",
        "Google Shopping / Google Product Category": "2667",
        "Google Shopping / AdWords Grouping": "Vehicles & Parts > Vehicle Parts & Accessories > Vehicle Maintenance, Care & Decor > Vehicle Decor",
        "Google Shopping / AdWords Labels": ""
    },
    {
        "Product": "greetingcard",
        "Product Category": "Arts & Entertainment > Party & Celebration > Gift Giving > Greeting & Note Cards",
        "Google Shopping / Google Product Category": "95",
        "Google Shopping / AdWords Grouping": "Party & Celebration",
        "Google Shopping / AdWords Labels": "Gift Giving"
    }
]






#==================================================================
#              Product_level_dictionary
#==================================================================

def product_level_dictionary(image_filename, output_folder_path, product_info_list):
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
        "Option1 Name": "Material",
        "Option1 Value": product_info_list["Option1 Value"],
        "Option2 Name": "Frame",
        "Option2 Value":product_info_list["Option2 Value"],
        "Option3 Name":"Size",
        "Option3 Value": product_info_list["Option3 Value"],
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
        "Variant Image": get_image_url_from_cloudinary(public_id),  # Use the Cloudinary URL,
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