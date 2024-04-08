"""Rename timetable_constraint to exam_timetable_constraint

Revision ID: 1e0254ee53f1
Revises: e91f00257569
Create Date: 2024-04-08 16:58:02.995235

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "1e0254ee53f1"
down_revision = "e91f00257569"
branch_labels = None
depends_on = None


def upgrade():
    exam_timetable_constraint = postgresql.ENUM(
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
        name="exam_timetable_constraint",
        create_type=False,
    )
    exam_timetable_constraint.create(op.get_bind(), checkfirst=False)

    op.add_column(
        "internal_module_on_offer",
        sa.Column(
            "exam_timetable_constraint", exam_timetable_constraint, nullable=True
        ),
    )
    op.drop_column("internal_module_on_offer", "timetable_constraint")
    op.execute("DROP TYPE timetable_constraint")


def downgrade():
    timetable_constraint = postgresql.ENUM(
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
        name="exam_timetable_constraint",
        create_type=False,
    )
    timetable_constraint.create(op.get_bind(), checkfirst=False)
    op.add_column(
        "internal_module_on_offer",
        sa.Column("timetable_constraint", timetable_constraint, nullable=True),
    )
    op.drop_column("internal_module_on_offer", "exam_timetable_constraint")
    op.execute("DROP TYPE exam_timetable_constraint")
