import os
import psycopg2
import csv
from extract_file_info_v5 import extract_file_info_v5
from dotenv import load_dotenv
from testDatabaseConnection import establish_connection, get_product_data_by_aspect_ratio, get_product_info_list

# Load environment variables from .env file
load_dotenv()

# Get the values of the environment variables
DB_USERNAME = os.getenv("PGUSER_2")
DB_PASSWORD = os.getenv("PGPASSWORD_2")


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
            SELECT ratio, material, frame_type, size, price
            FROM product_frame_size_price_50
            WHERE ratio = %s
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

get_product_data_by_aspect_ratio(conn, 0.67)