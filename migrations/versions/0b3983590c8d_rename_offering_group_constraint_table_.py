"""Rename offering_group_constraint table to offering_group

Revision ID: 0b3983590c8d
Revises: 9af090b71582
Create Date: 2024-03-26 14:47:39.434128

"""
import sqlalchemy as sa
import sqlmodel  # added
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0b3983590c8d"
down_revision = "9af090b71582"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "offering_group",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "label",
            postgresql.ENUM(
                "OPTIONAL", "SELECTIVE", name="offering_group_label", create_type=False
            ),
            nullable=False,
        ),
        sa.Column("min", sa.Integer(), nullable=False),
        sa.Column("max", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.drop_table("offering_group_constraint")


def downgrade():
    op.create_table(
        "offering_group_constraint",
        sa.Column(
            "offering_group",
            postgresql.ENUM(
                "OPTIONAL", "SELECTIVE", name="offering_group_label", create_type=False
            ),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("year", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("min", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("max", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="offering_group_constraint_pkey"),
    )
    op.drop_table("offering_group")
