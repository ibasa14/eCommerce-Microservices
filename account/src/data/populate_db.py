import os

import psycopg2


def populate_user_table():
    # Connect to the database
    conn = psycopg2.connect(
        f'{os.environ.get("POSTGRES_SCHEMA")}://{os.environ.get("POSTGRES_USERNAME")}:{os.environ.get("POSTGRES_PASSWORD")}@{os.environ.get("POSTGRES_HOST")}:{os.environ.get("POSTGRES_PORT")}/{os.environ.get("POSTGRES_DB")}'
    )

    with conn.cursor() as curs:
        try:
            # Define the SQL statement
            populate_query = """
            DELETE FROM users;
            INSERT INTO users(name,
                            email,
                            hashed_password,
                            is_active,
                            is_logged_in,
                            role_id)
            VALUES ('admin',
                    'admin@ibc.com',
                    '$2b$12$zX6L9xYc82wiy5VxE8igT.isAdFbYs7zwXddSfk/uaxmk/ot.CWae',
                    true,
                    false,
                    1);
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
        populate_user_table()
