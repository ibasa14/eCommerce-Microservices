from alembic import op

POPULATE_CATEGORY_TABLE: str = """
    INSERT INTO categories(name)
    VALUES ('meat'),
            ('seafood'),
            ('beverage'),
            ('nonfood'),
            ('bakery');
"""


def populate_role_and_category() -> None:
    op.execute(POPULATE_CATEGORY_TABLE)


def clean_role_and_category() -> None:
    op.execute("DELETE FROM categories;")
