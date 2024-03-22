from alembic import op

POPULATE_ROLE_TABLE: str = """
    INSERT INTO roles(name)
    VALUES ('admin'),
           ('client');
"""


def populate_role() -> None:
    op.execute(POPULATE_ROLE_TABLE)


def clean_role() -> None:
    op.execute("DELETE FROM roles;")
