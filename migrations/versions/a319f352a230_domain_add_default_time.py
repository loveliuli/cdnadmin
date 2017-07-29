"""domain add default time

Revision ID: a319f352a230
Revises: 7135e76d08eb
Create Date: 2017-07-28 09:44:28.788647

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a319f352a230'
down_revision = '7135e76d08eb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'domain', 'project', ['project_id'], ['id'])
    op.create_foreign_key(None, 'user_projects', 'user', ['user_id'], ['id'])
    op.create_foreign_key(None, 'user_projects', 'project', ['project_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_projects', type_='foreignkey')
    op.drop_constraint(None, 'user_projects', type_='foreignkey')
    op.drop_constraint(None, 'domain', type_='foreignkey')
    # ### end Alembic commands ###