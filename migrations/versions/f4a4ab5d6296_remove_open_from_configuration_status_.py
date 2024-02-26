"""Remove OPEN from configuration.status enum

Revision ID: f4a4ab5d6296
Revises: b4037303e321
Create Date: 2024-02-26 12:16:17.782025

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f4a4ab5d6296"
down_revision = "b4037303e321"
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Rename the old enum type (PostgreSQL specific SQL)
    op.execute(
        "ALTER TYPE module_selection_status RENAME TO module_selection_status_old"
    )

    # Step 2: Create new enum type without 'OPEN'
    new_enum = sa.Enum("CLOSED", "USE_PERIODS", name="module_selection_status")
    new_enum.create(op.get_bind(), checkfirst=False)

    # Step 3: Update rows from 'OPEN' to 'USE_PERIODS'
    op.execute("UPDATE configuration SET status = 'USE_PERIODS' WHERE status = 'OPEN'")

    # Step 4: Alter the column to use the new enum type
    op.alter_column(
        "configuration",
        "status",
        type_=new_enum,
        existing_type=sa.Enum(name="module_selection_status_old"),
        nullable=False,
        postgresql_using="status::text::module_selection_status",
    )

    # Step 5: Drop the old enum type
    op.execute("DROP TYPE module_selection_status_old")


def downgrade():
    # Step 1: Rename the current enum type
    op.execute(
        "ALTER TYPE module_selection_status RENAME TO module_selection_status_new"
    )

    # Step 2: Recreate the old enum type including 'OPEN'
    old_enum = sa.Enum("OPEN", "CLOSED", "USE_PERIODS", name="module_selection_status")
    old_enum.create(op.get_bind(), checkfirst=False)

    # Step 3: Alter the column to use the old enum type
    op.alter_column(
        "configuration",
        "status",
        type_=old_enum,
        existing_type=sa.Enum(name="module_selection_status_new"),
        nullable=False,
    )

    # Step 4: Drop the new enum type
    op.execute("DROP TYPE module_selection_status_new")
