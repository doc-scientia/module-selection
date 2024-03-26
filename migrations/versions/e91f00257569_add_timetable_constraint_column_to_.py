"""Add timetable_constraint column to internal_module_on_offer

Revision ID: e91f00257569
Revises: c41c1e8b2829
Create Date: 2024-03-26 16:57:25.429155

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "e91f00257569"
down_revision = "c41c1e8b2829"
branch_labels = None
depends_on = None


def upgrade():
    timetable_constraint_enum = postgresql.ENUM(
        "Tx101",
        "Tx102",
        "Tx103",
        "Tx104",
        "Tx105",
        "Tx106",
        "Tx107",
        "Tx108",
        "Tx109",
        "Tx201",
        "Tx202",
        "Tx203",
        "Tx204",
        "Tx205",
        "Tx206",
        "Tx207",
        "Tx208",
        "Tx209",
        name="timetable_constraint",
        create_type=True,
    )
    timetable_constraint_enum.create(op.get_bind(), checkfirst=True)
    op.add_column(
        "internal_module_on_offer",
        sa.Column("timetable_constraint", timetable_constraint_enum, nullable=True),
    )


def downgrade():
    op.drop_column("internal_module_on_offer", "timetable_constraint")
