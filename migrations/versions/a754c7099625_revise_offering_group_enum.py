"""Revise offering group enum

Revision ID: a754c7099625
Revises: a2edfd802c86
Create Date: 2024-04-15 10:18:40.930749

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "a754c7099625"
down_revision = "a2edfd802c86"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'OPTIONAL1'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'OPTIONAL2'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'OPTIONAL3'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'REQUIRED'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'REQUIRED1'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'REQUIRED2'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'REQUIRED3'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SELECTIVE1'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SELECTIVE2'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SELECTIVE3'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SELECTIVE4'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SUBTOTAL'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SUBTOTAL1'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SUBTOTAL2'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'SUBTOTAL3'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'EXTRACURRICULAR'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'XOR'")
    op.execute("ALTER TYPE offering_group_label ADD VALUE 'XOR1'")


def downgrade():
    pass
