import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from dotenv import load_dotenv
import os
import cloudinary
from cloudinary import uploader, api
from hashlib import md5

def generate_unique_identifier(image_path):
    # Generate a unique identifier for the image
    with open(image_path, 'rb') as file:
        content = file.read()
        checksum = md5(content).hexdigest()
        file_name = os.path.basename(image_path)
        unique_identifier = f"{file_name}_{checksum}"
        return unique_identifier


def check_existing_image(unique_id, unique_identifier):
    # Set up Cloudinary configuration
    load_dotenv()
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET"),
        # secure=os.getenv("CLOUDINARY_SECURE").lower() == "true"
    )

    try:
        search_results = cloudinary.api.resources_by_context(
            key=unique_id,
            value=unique_identifier,
            type="upload"
        )
        print("Search Results: ", search_results)  # Add this line for debugging
        return len(search_results["resources"]) > 0
    except cloudinary.exceptions.NotFound:
        return False



def upload_to_cloudinary(image_path):
    unique_identifier = generate_unique_identifier(image_path)

    if check_existing_image('image_hash', unique_identifier):  # Use 'image_hash' instead of 'unique_id_here'
        print("Image already exists in Cloudinary. Retrieving public_id.")

        # Get the public_id from the existing image
        search_results = cloudinary.api.resources_by_context(
            key='image_hash',
            value=unique_identifier,
            type="upload"
        )
        public_id = search_results['resources'][0]['public_id']
        return public_id

    # Upload the image to Cloudinary
    try:
        response = cloudinary.uploader.upload(image_path, context={"image_hash": unique_identifier})
        if response.get("public_id"):
            print(f"Uploaded image with public ID: {response['public_id']}")
            return response['public_id']
        else:
            print("Failed to upload image to Cloudinary.")
            return None
    except Exception as e:
        print(f"Error during image upload: {e}")
        return None


def get_image_url_from_cloudinary(public_id):
    if public_id is None:
        return None
    resource = cloudinary.api.resource(public_id)
    return resource["url"]


