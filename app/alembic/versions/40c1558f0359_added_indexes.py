"""Added indexes

Revision ID: 40c1558f0359
Revises: 28218b15b8d7
Create Date: 2025-03-23 18:41:55.971882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '40c1558f0359'
down_revision: Union[str, None] = '28218b15b8d7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_commits_engineer_id'), 'commits', ['engineer_id'], unique=False)
    op.create_index(op.f('ix_commits_jira_issue_id'), 'commits', ['jira_issue_id'], unique=False)
    op.create_index(op.f('ix_engineers_team_id'), 'engineers', ['team_id'], unique=False)
    op.create_index(op.f('ix_repositories_project_id'), 'repositories', ['project_id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_repositories_project_id'), table_name='repositories')
    op.drop_index(op.f('ix_engineers_team_id'), table_name='engineers')
    op.drop_index(op.f('ix_commits_jira_issue_id'), table_name='commits')
    op.drop_index(op.f('ix_commits_engineer_id'), table_name='commits')
    # ### end Alembic commands ###
