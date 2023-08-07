def process_image(output_folder_path):
    def sort_sku(variant):
        # Split the SKU into numeric and non-numeric parts
        parts = variant.get("Variant SKU", "").split("-")
        numeric_part = int(parts[0]) if parts and parts[0].isdigit() else 0
        return numeric_part

    image_list = []
    handle_dict = count_files_by_handle(output_folder_path)

    for filename in os.listdir(output_folder_path):
        file_path = os.path.join(output_folder_path, filename)
        file_info = extract_file_info_v5(file_path)

        # Check if file_info is not None before proceeding
        if file_info is not None:
            handle = file_info["handle"]
            image_position = int(file_info["image_position_var"])
            product_info_list = get_product_info_list(file_path)
            
            if filename.endswith((".jpg", ".jpeg", ".png", ".webp")):
                if image_position == 1:
                    product_info_list_1 = product_info_list[0]
                    image_list.append(product_level_dictionary(filename, output_folder_path, product_info_list_1))
                    image_list.extend(product_info_list[handle_dict[handle]:])
                elif image_position == 2:
                    product_info_list_2 = product_info_list[1]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_2))
                elif image_position == 3:
                    product_info_list_3 = product_info_list[2]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_3))
                elif image_position == 4:
                    product_info_list_4 = product_info_list[3]
                    image_list.append(variant_level_dictionary(filename, output_folder_path, product_info_list_4))

    # Sort image_list by Variant SKU first
    image_list.sort(key=sort_sku)

    # Group image_list by handle
    grouped_image_list = []
    for handle, variants in itertools.groupby(image_list, key=lambda x: x.get("handle")):
        grouped_image_list.extend(sorted(variants, key=sort_sku))

    return grouped_image_list




def count_files_by_handle(output_folder_path):
    handle_dict = {}
    for filename in os.listdir(output_folder_path):
        file_path = os.path.join(output_folder_path, filename)
        file_info = extract_file_info_v5(file_path)

        # Check if file_info is not None before proceeding
        if file_info is not None:
            handle = file_info["handle"]
            if handle in handle_dict:
                handle_dict[handle] += 1
            else:
                handle_dict[handle] = 1

    return handle_dict