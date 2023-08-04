image_list = [{'Handle': '1a6d85', 
               'Title': 'City in Purple Sunset', 
               'Vendor': 'obl display ss', 
               'Image Src': 'http://res.cloudinary.com/djqvqmqe2/image/upload/v1689915804/j30adxkx6ggmm4ywnfea.jpg', 
               'Image Alt Text': 'City in Purple Sunset', 
}]

table_name = "shopifyproduct"


def create_insert_statement(image_list, table_name):
    columns = image_list[0].keys()
    values = []
    for image_dict in image_list:
        value_strings = []
        for key, value in image_dict.items():
            if isinstance(value, str):
                value_strings.append(f"'{value}'")
            else:
                value_strings.append(str(value))
        values.append("(" + ", ".join(value_strings) + ")")

    insert_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {', '.join(values)};"
    return insert_query


results = create_insert_statement(image_list,table_name)
