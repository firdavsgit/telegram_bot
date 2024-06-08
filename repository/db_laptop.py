import psycopg2

class Postgres():
    def __init__(self):

        self.data_base = psycopg2.connect(
                        host='localhost',
                        user='postgres',
                        database='laptop',
                        password='123456'

        )
        self.cursor = self.data_base.cursor()


    def table_create(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS laptops (
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
            INSERT INTO laptops (product_name, description, product_f_name,product_f_value , product_price, product_image) 
            VALUES
             (%s, %s, %s, %s, %s, %s)      
        """, args)
        return self.data_base.commit()


    def select_data(self):
        """select data"""
        self.cursor.execute("""
            SELECT product_f_value, product_image, product_name, product_price 
            FROM laptops
        """)
        return self.cursor.fetchall()


Postgres().select_data()

