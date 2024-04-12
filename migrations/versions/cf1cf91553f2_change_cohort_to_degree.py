"""Change cohort to degree

Revision ID: cf1cf91553f2
Revises: 41376ffffe93
Create Date: 2024-04-12 15:42:03.722577

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "cf1cf91553f2"
down_revision = "41376ffffe93"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("ALTER TABLE cohort_regulations RENAME COLUMN cohort TO degree")
    op.execute(
        "ALTER TABLE cohort_regulations RENAME CONSTRAINT cohort_regulations_pkey TO degree_regulations_pkey"
    )
    op.execute(
        "ALTER TABLE cohort_regulations RENAME CONSTRAINT cohort_regulations_module_id_fkey TO degree_regulations_module_id_fkey"
    )
    op.execute(
        "ALTER TABLE cohort_regulations RENAME CONSTRAINT cohort_regulations_offering_group_id_fkey TO degree_regulations_offering_group_id_fkey"
    )
    op.execute(
        "ALTER SEQUENCE cohort_regulations_id_seq RENAME TO degree_regulations_id_seq"
    )
    op.execute("ALTER TABLE cohort_regulations RENAME TO degree_regulations")
    op.drop_index("ix_cohort_regulations_module_id", table_name="cohort_regulations")
    op.create_index(
        op.f("ix_degree_regulations_module_id"),
        "degree_regulations",
        ["module_id"],
        unique=False,
    )

    # Relation with internal_module_choice
    op.add_column(
        "internal_module_choice",
        sa.Column("degree_regulations_id", sa.Integer(), nullable=False),
    )
    op.drop_constraint(
        "internal_module_choice_cohort_regulations_id_username_key",
        "internal_module_choice",
        type_="unique",
    )
    op.drop_index(
        "ix_internal_module_choice_cohort_regulations_id",
        table_name="internal_module_choice",
    )
    op.create_index(
        op.f("ix_internal_module_choice_degree_regulations_id"),
        "internal_module_choice",
        ["degree_regulations_id"],
        unique=False,
    )
    op.create_unique_constraint(
        None, "internal_module_choice", ["degree_regulations_id", "username"]
    )
    op.drop_constraint(
        "internal_module_choice_cohort_regulations_id_fkey",
        "internal_module_choice",
        type_="foreignkey",
    )
    op.create_foreign_key(
        None,
        "internal_module_choice",
        "degree_regulations",
        ["degree_regulations_id"],
        ["id"],
    )
    op.drop_column("internal_module_choice", "cohort_regulations_id")


def downgrade():
    op.execute("ALTER TABLE degree_regulations RENAME COLUMN degree TO cohort")
    op.execute(
        "ALTER TABLE degree_regulations RENAME CONSTRAINT degree_regulations_pkey TO cohort_regulations_pkey"
    )
    op.execute(
        "ALTER TABLE degree_regulations RENAME CONSTRAINT degree_regulations_module_id_fkey TO cohort_regulations_module_id_fkey"
    )
    op.execute(
        "ALTER TABLE degree_regulations RENAME CONSTRAINT degree_regulations_offering_group_id_fkey TO cohort_regulations_offering_group_id_fkey"
    )
    op.execute(
        "ALTER SEQUENCE degree_regulations_id_seq RENAME TO cohort_regulations_id_seq"
    )
    op.execute("ALTER TABLE degree_regulations RENAME TO cohort_regulations")
    op.add_column(
        "internal_module_choice",
        sa.Column(
            "cohort_regulations_id", sa.INTEGER(), autoincrement=False, nullable=False
        ),
    )
    op.drop_constraint(
        "internal_module_choice_degree_regulations_id_fkey",
        "internal_module_choice",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "internal_module_choice_cohort_regulations_id_fkey",
        "internal_module_choice",
        "cohort_regulations",
        ["cohort_regulations_id"],
        ["id"],
    )
    op.drop_constraint(
        "internal_module_choice_degree_regulations_id_username_key",
        "internal_module_choice",
        type_="unique",
    )
    op.drop_index(
        op.f("ix_internal_module_choice_degree_regulations_id"),
        table_name="internal_module_choice",
    )
    op.create_index(
        "ix_internal_module_choice_cohort_regulations_id",
        "internal_module_choice",
        ["cohort_regulations_id"],
        unique=False,
    )
    op.create_unique_constraint(
        "internal_module_choice_cohort_regulations_id_username_key",
        "internal_module_choice",
        ["cohort_regulations_id", "username"],
    )
    op.drop_column("internal_module_choice", "degree_regulations_id")
    op.create_index(
        "ix_cohort_regulations_module_id",
        "cohort_regulations",
        ["module_id"],
        unique=False,
    )
    op.drop_index(
        op.f("ix_degree_regulations_module_id"), table_name="degree_regulations"
    )
