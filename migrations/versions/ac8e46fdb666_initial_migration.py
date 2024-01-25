"""Initial migration

Revision ID: ac8e46fdb666
Revises:
Create Date: 2023-08-09 17:44:11.137781

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "ac8e46fdb666"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "tutoring_session",
        sa.Column("group", sa.String(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("year", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "tutoring_session_attendance",
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("present", sa.Boolean(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("tutoring_session_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["tutoring_session_id"],
            ["tutoring_session.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_tutoring_session_attendance_tutoring_session_id"),
        "tutoring_session_attendance",
        ["tutoring_session_id"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_tutoring_session_attendance_tutoring_session_id"),
        table_name="tutoring_session_attendance",
    )
    op.drop_table("tutoring_session_attendance")
    op.drop_table("tutoring_session")
