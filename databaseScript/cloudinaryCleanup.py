import os
import requests
import json
import cloudinary
import cloudinary.uploader
import cloudinary.api
from urllib.parse import urlsplit
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Set up Cloudinary configuration
cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = os.getenv("CLOUDINARY_SECURE").lower() == "true"
)

# Shopify API credentials
API_KEY = os.getenv("SHOPIFY_API_KEY")
API_PASSWORD = os.getenv("SHOPIFY_API_PASSWORD")
SHOP_DOMAIN = os.getenv("SHOPIFY_SHOP_DOMAIN")

def get_shopify_images():
    url = f"https://{API_KEY}:{API_PASSWORD}@{SHOP_DOMAIN}/admin/api/2021-07/products.json?fields=id,title,images"
    response = requests.get(url)
    print(response.text)  # print the response for debugging
    if response.status_code == 200:
        data = response.json()
        product_image_pairs = []
        for product in data["products"]:
            for image in product["images"]:
                product_image_pairs.append((product, image))  # Append a tuple with the product and image dictionary
        return product_image_pairs
    else:
        print("Failed to fetch Shopify images.")
        return []



if __name__ == "__main__":
    # Get the list of Shopify images
    product_image_pairs = get_shopify_images()

    # Initialize shopify_image_names as an empty list
    shopify_image_names = []

    if product_image_pairs is not None:
        # Extract image URLs
        images = [pair[1]["src"] for pair in product_image_pairs]
    
        # Create the 'asset_txt' folder if it doesn't exist
        folder_name = 'asset_txt'
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        # Generate a timestamp for the filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        
        # Specify the filename with the timestamp
        filename = f"shopify_images_{timestamp}.txt"
        
        # Specify the file path
        file_path = os.path.join(folder_name, filename)
        
        # Write Shopify images to the text file
        with open(file_path, 'w') as f:
            for pair in product_image_pairs:
                f.write(json.dumps(pair) + '\n')
        
        # Extract image file names from the Shopify image URLs
        shopify_image_names = [os.path.splitext(urlsplit(url).path.split("/")[-1])[0] for url in images]
    else:
        print("No product-image pairs retrieved.")

    # Get all resources (images) from Cloudinary
    all_resources = cloudinary.api.resources()

    for resource in all_resources['resources']:
        # Check if this resource is not in use on Shopify
        if resource['public_id'] not in shopify_image_names:
            # Print the resource that is going to be deleted
            print(f"Deleting image: {resource['url']}")
            # Delete the resource
            cloudinary.uploader.destroy(resource['public_id'])



def write_cloudinary_image_metadata_to_file(filename):
    # Set up Cloudinary configuration
    load_dotenv()
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        secure=os.getenv("CLOUDINARY_SECURE").lower() == "true"
    )

    # Get all resources (images) from Cloudinary
    all_resources = cloudinary.api.resources()

    # Create a list to store image metadata dictionaries
    metadata_list = []

    # Collect image metadata
    for resource in all_resources['resources']:
        metadata = {
            "image_id": resource['public_id'],
            "url": resource['url'],
            "type": resource['type'],
            "format": resource['format'],
            "created_at": resource['created_at'],
            "width": resource['width'],
            "height": resource['height'],
            "bytes": resource['bytes']
        }
        metadata_list.append(metadata)

    # Specify the folder name
    folder_name = "asset_txt"

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Generate a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Specify the filename with the timestamp
    filename = f"image_metadata_{timestamp}.txt"

    # Specify the file path
    file_path = os.path.join(folder_name, filename)

    # Write metadata to a text file
    with open(file_path, 'w') as file:
        json.dump(metadata_list, file, indent=4)

# Specify the filename to save the metadata
filename = "image_metadata.txt"
write_cloudinary_image_metadata_to_file(filename)

