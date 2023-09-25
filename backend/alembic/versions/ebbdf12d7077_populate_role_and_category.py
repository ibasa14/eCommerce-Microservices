"""populate role and category

Revision ID: ebbdf12d7077
Revises: a1b0d81311c4
Create Date: 2023-09-25 18:11:38.789696

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "ebbdf12d7077"
down_revision: Union[str, None] = "a1b0d81311c4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

POPULATE_ROLE_TABLE = """
INSERT INTO roles(name)
VALUES ('admin'),
       ('client');
"""

POPULATE_CATEGORY_TABLE = """
INSERT INTO categories(name)
VALUES ('meat'),
        ('seafood'),
        ('beverage'),
        ('nonfood'),
        ('bakery');
"""


def upgrade() -> None:
    op.execute(POPULATE_ROLE_TABLE)
    op.execute(POPULATE_CATEGORY_TABLE)


def downgrade() -> None:
    op.execute("DELETE FROM roles;")
    op.execute("DELETE FROM categories;")
