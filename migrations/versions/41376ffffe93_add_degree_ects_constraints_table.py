"""Add degree_ects_constraints table

Revision ID: 41376ffffe93
Revises: 1e0254ee53f1
Create Date: 2024-04-09 16:36:38.185880

"""
import sqlalchemy as sa
import sqlmodel  # added
from alembic import op

# revision identifiers, used by Alembic.
revision = "41376ffffe93"
down_revision = "1e0254ee53f1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "degree_ects_constraints",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("degree", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("min", sa.Float(), nullable=False),
        sa.Column("max", sa.Float(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("degree_ects_constraints")
