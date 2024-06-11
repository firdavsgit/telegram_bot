import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

class Postgres_monitor():
    def __init__(self):
        self.data_base = psycopg2.connect(
            host=os.getenv('HOST'),
            user=os.getenv('USER'),
            database=os.getenv('DATABASE'),
            password=os.getenv('PASSWORD')

        )
        self.cursor = self.data_base.cursor()

    def table_create(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS monitors (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(255),
                description TEXT,
                product_f_name VARCHAR(255),
                product_f_value VARCHAR(255),
                product_price VARCHAR(255),
                product_image VARCHAR(255)
            )

        """)

    def insert(self, *args):
        self.table_create()
        self.cursor.execute(f"""
            INSERT INTO monitors (product_name, description, product_f_name,product_f_value , product_price, product_image) 
            VALUES
             (%s, %s, %s, %s, %s, %s)      
        """, args)
        return self.data_base.commit()

    def select_data(self):
        self.cursor.execute("""
            SELECT product_f_value, product_image, product_name, product_price 
            FROM monitors
        """)
        return self.cursor.fetchall()