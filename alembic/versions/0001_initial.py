from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"), sa.UniqueConstraint("username"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)
    op.create_table("accounts",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("number", sa.String(20), nullable=False),
        sa.Column("balance", sa.Numeric(15,2), nullable=False, server_default=sa.text("0.00")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"), sa.UniqueConstraint("number"),
    )
    op.create_index("ix_accounts_number", "accounts", ["number"], unique=True)
    op.create_table("transactions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("type", sa.Enum("deposit","withdrawal","transfer", name="transactiontype"), nullable=False),
        sa.Column("amount", sa.Numeric(15,2), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.Column("target_account_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["account_id"], ["accounts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_account_id"], ["accounts.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

def downgrade() -> None:
    op.drop_table("transactions")
    op.drop_index("ix_accounts_number", "accounts"); op.drop_table("accounts")
    op.drop_index("ix_users_username", "users"); op.drop_index("ix_users_email", "users")
    op.drop_table("users")
