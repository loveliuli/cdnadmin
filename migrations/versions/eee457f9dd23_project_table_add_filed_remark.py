"""project table add filed remark

Revision ID: eee457f9dd23
Revises: 6942df84ce38
Create Date: 2017-10-10 14:37:53.629888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eee457f9dd23'
down_revision = '6942df84ce38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'domain', 'project', ['project_id'], ['id'])
    op.add_column('project', sa.Column('remark', sa.String(length=255), nullable=True))
    op.create_foreign_key(None, 'role_users', 'role', ['role_id'], ['id'])
    op.create_foreign_key(None, 'role_users', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'user_projects', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'user_projects', 'project', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_projects', type_='foreignkey')
    op.drop_constraint(None, 'user_projects', type_='foreignkey')
    op.drop_constraint(None, 'role_users', type_='foreignkey')
    op.drop_constraint(None, 'role_users', type_='foreignkey')
    op.drop_column('project', 'remark')
    op.drop_constraint(None, 'domain', type_='foreignkey')
    # ### end Alembic commands ###
