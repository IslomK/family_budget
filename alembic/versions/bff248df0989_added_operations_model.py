"""Added operations model

Revision ID: bff248df0989
Revises: 4244aa7ebdd9
Create Date: 2022-11-30 16:06:32.258707

"""
from sqlalchemy.dialects import postgresql
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "bff248df0989"
down_revision = "4244aa7ebdd9"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "operation",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("title", sa.String(length=32), nullable=True),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("budget_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_by_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("commentary", sa.Text(), nullable=True),
        sa.Column(
            "operation_type",
            sa.Enum("OUTCOMES", "INCOMES", name="operationtypeenum"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["budget_id"],
            ["budget.id"],
        ),
        sa.ForeignKeyConstraint(
            ["created_by_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_operation_budget_id"), "operation", ["budget_id"], unique=False)
    op.create_index(
        op.f("ix_operation_created_by_id"), "operation", ["created_by_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_operation_created_by_id"), table_name="operation")
    op.drop_index(op.f("ix_operation_budget_id"), table_name="operation")
    op.drop_table("operation")
    op.execute(
        """
        DROP TYPE operationtypeenum;
        """
    )
    # ### end Alembic commands ###
