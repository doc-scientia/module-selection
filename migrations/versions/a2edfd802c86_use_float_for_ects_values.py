"""Use float for ects values

Revision ID: a2edfd802c86
Revises: cf1cf91553f2
Create Date: 2024-04-12 17:59:14.802495

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "a2edfd802c86"
down_revision = "cf1cf91553f2"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
        "degree_regulations",
        "ects",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )
    op.alter_column(
        "offering_group",
        "min",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )
    op.alter_column(
        "offering_group",
        "max",
        existing_type=sa.INTEGER(),
        type_=sa.Float(),
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "offering_group",
        "max",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "offering_group",
        "min",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
    op.alter_column(
        "degree_regulations",
        "ects",
        existing_type=sa.Float(),
        type_=sa.INTEGER(),
        existing_nullable=False,
    )
