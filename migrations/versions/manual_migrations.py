from alembic import op

# revision identifiers, used by Alembic.


revision = "4057e8868ce8"
down_revision = "4057e8868ce7"
branch_labels = None
depends_on = None


def upgrade():
    op.execute("UPDATE address SET std_code = std_code*2")


def downgrade():
    op.execute("UPDATE address SET std_code = std_code/2")
