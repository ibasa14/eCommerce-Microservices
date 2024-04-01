import os

import psycopg2


def populate_product_table():
    # Connect to the database
    conn = psycopg2.connect(
        f'{os.environ.get("POSTGRES_SCHEMA")}://{os.environ.get("POSTGRES_USERNAME")}:{os.environ.get("POSTGRES_PASSWORD")}@{os.environ.get("POSTGRES_HOST")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB")}'
    )

    with conn.cursor() as curs:
        try:
            # Define the SQL statement
            populate_query = """
            DELETE FROM products;
            INSERT INTO products(name, description, price, stock, category_id)
            VALUES ('product1', 'description1', 22.3, 5, 1),
                ('product2', 'description2', 2.3, 10, 2),
                ('product3', 'description3', 122.3, 20, 3),
                ('product4', 'description4', 5.3, 40, 4),
                ('product5', 'description5', 7.99, 50, 2),
                ('product6', 'description6', 8.3, 10, 1),
                ('product7', 'description7', 5.5, 40, 2)
            """

            # Execute the SQL statement
            curs.execute(populate_query)
            # Commit the changes and close the connection
            conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


if __name__ == "__main__":
    # Call the function to populate the table
    if os.environ.get("ENVIRONMENT") == "DEV":
        populate_product_table()
