"""Rename offering_group enum to offering_group_label

Revision ID: 9af090b71582
Revises: 42af62166d24
Create Date: 2024-03-26 14:36:03.331815

"""
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "9af090b71582"
down_revision = "42af62166d24"
branch_labels = None
depends_on = None


def upgrade():
    # Create the new enum type 'offering_group_label' in PostgreSQL
    offering_group_label = postgresql.ENUM(
        "OPTIONAL", "SELECTIVE", name="offering_group_label", create_type=False
    )
    offering_group_label.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE cohort_regulations ALTER COLUMN offering_group TYPE offering_group_label USING offering_group::text::offering_group_label"
    )
    op.execute(
        "ALTER TABLE offering_group_constraint ALTER COLUMN offering_group TYPE offering_group_label USING offering_group::text::offering_group_label"
    )
    op.execute("DROP TYPE offering_group")


def downgrade():
    # Recreate the dropped enum type 'offering_group'
    offering_group = postgresql.ENUM(
        "OPTIONAL", "SELECTIVE", name="offering_group", create_type=False
    )
    offering_group.create(op.get_bind(), checkfirst=False)
    op.execute(
        "ALTER TABLE cohort_regulations ALTER COLUMN offering_group TYPE offering_group USING offering_group::text::offering_group"
    )
    op.execute(
        "ALTER TABLE offering_group_constraint ALTER COLUMN offering_group TYPE offering_group USING offering_group::text::offering_group"
    )
    op.execute("DROP TYPE offering_group_label")
