import os
import psycopg2
import csv
from extract_file_info_v5 import extract_file_info_v5
from dotenv import load_dotenv



DB_USERNAME = "obljjawa"
DB_PASSWORD = "ZUtHPbXd5B9L"

# Modify the function to use environment variables for username and password
def establish_connection():
    try:
        # Construct the connection string using environment variables
        conn_str = f"postgres://{DB_USERNAME}:{DB_PASSWORD}@ep-red-limit-009953.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
        conn = psycopg2.connect(conn_str)
        print("Connection established successfully!")
        return conn
    except psycopg2.Error as e:
        print("Error: Unable to connect to the database.")
        print(e)
        return None


# Define the function to get product data by aspect ratio
def get_product_data_by_aspect_ratio(conn, aspect_ratio):
    try:
        cursor = conn.cursor()

        # Prepare the SQL query with placeholders for aspect_ratio
        sql_query = """
            SELECT *
            FROM product_frame_size_price_setof2
            WHERE ratio = %s
            ORDER BY ratio, material,
                CASE frame_type
                    WHEN 'Gallery Wrap' THEN 1
                    WHEN 'White Floating Frame' THEN 2
                    WHEN 'Black Floating Frame' THEN 3
                    WHEN 'Golden Floating Frame' THEN 4
                    WHEN 'White Frame' THEN 6
                    WHEN 'Black Frame' THEN 7
                    WHEN 'Brown Frame' THEN 8
                    WHEN 'White Frame With Mount' THEN 9
                    WHEN 'Black Frame With Mount' THEN 10
                    WHEN 'Brown Frame With Mount' THEN 11
                    WHEN 'Rolled Art' THEN 12
                    ELSE 13
            END,
            CAST(SUBSTRING(size FROM '^[0-9]+') AS INTEGER),
            size;
            """

        # Execute the query passing the aspect_ratio as a tuple in the second argument
        cursor.execute(sql_query, (aspect_ratio,))

        # Fetch all rows from the result set
        product_data = cursor.fetchall()

        # Close the cursor
        cursor.close()

        return product_data
    except psycopg2.Error as e:
        print("Error: Unable to fetch data from the database.")
        print(e)
        return []



def get_product_info_list_setOf2(image_filename, image_url_list):
    # Establish the connection to the PostgreSQL database
    connection = establish_connection()

    if connection:
        # Extract image information from filename
        file_info = extract_file_info_v5(image_filename)
        aspect_ratio = file_info["aspect_ratio"]
        product_data = get_product_data_by_aspect_ratio(connection, aspect_ratio)
        artist = file_info["vendor"]

        # Transform the product_data into a list of dictionaries
        product_info_list = []
        for i, data_row in enumerate(product_data):

            variant_sku = f"{i + 1}-{file_info['handle']}"
        
            # Find the dictionary with matching "Variant SKU" in the image_url_list
            matching_dict = next((item for item in image_url_list if item["Variant SKU"] == variant_sku), None)

            product_info = {
                "Handle": file_info["handle"],
                "Option1 Value": data_row[2],   # Material
                "Option2 Value": data_row[3],   # Frame Type
                "Option3 Value": data_row[4],   # Size
                "Variant Price": data_row[5],    # Price
                "Variant Inventory Policy": "deny",
                "Variant Fulfillment Service": "manual",
                "Variant SKU": variant_sku,
                "Variant Inventory Qty": 10,
                "Variant Image": matching_dict["Image URL"] if matching_dict else ""  # Get the image URL from the matching_dict
                
            }
            product_info_list.append(product_info)

        # Don't forget to close the connection when you're done
        connection.close()

        return product_info_list