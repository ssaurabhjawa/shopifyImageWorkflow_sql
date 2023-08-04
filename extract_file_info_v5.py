import os



def extract_file_info_v5(file_path):
    # Extract file name from file path
    file_name = os.path.basename(file_path)
    # Split file name into parts based on delimiter
    file_parts = file_name.split("--")

    # Check if the file name has the expected number of parts
    if len(file_parts) < 6:
        # Handle the error gracefully (you can choose to log the error or skip the file)
        print(f"Error: Invalid filename format for {file_name}")
        return None

    # Extract variables from file parts
    aspect_ratio = (file_parts[0])
    uuid = file_parts[1]
    product_material = file_parts[2].lower()
    title_var = file_parts[3]
    image_position_var = int(file_parts[4])
    artist_name = os.path.splitext(file_parts[5])[0].lower()

    # Create dictionary containing the extracted variables
    file_info = {
        "aspect_ratio": float(aspect_ratio),
        "handle": uuid,
        "title": title_var,
        "image_position_var": image_position_var,
        "vendor": artist_name,
        "product_material": product_material,
    }

    return file_info
