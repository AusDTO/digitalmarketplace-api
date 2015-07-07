"""empty message

Revision ID: 180_remove_user_locked_flag
Revises: 170_add_login_tracking
Create Date: 2015-07-03 16:07:45.172143

"""

# revision identifiers, used by Alembic.
revision = '180_remove_user_locked_flag'
down_revision = '170_add_login_tracking'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'locked')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('locked', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.execute('UPDATE users SET locked=FALSE WHERE failed_login_count < 6;')
    op.execute('UPDATE users SET locked=TRUE WHERE failed_login_count >= 6;')
    op.alter_column('users', 'locked', nullable=False)
    ### end Alembic commands ###