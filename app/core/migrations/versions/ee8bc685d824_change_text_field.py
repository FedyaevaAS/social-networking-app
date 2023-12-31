"""change text field

Revision ID: ee8bc685d824
Revises: 9b0da34cd0dc
Create Date: 2023-07-18 11:49:04.006166

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ee8bc685d824"
down_revision = "9b0da34cd0dc"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, "posts", ["text"])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "posts", type_="unique")
    # ### end Alembic commands ###
