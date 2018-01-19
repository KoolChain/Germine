"""empty message

Revision ID: c5fd558d2799
Revises:
Create Date: 2018-01-18 17:40:18.929904

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'c5fd558d2799'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('currency', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f('uq_currency_name'), ['name']
        )
        batch_op.create_unique_constraint(
            batch_op.f('uq_currency_symbol'), ['symbol']
        )

    with op.batch_alter_table('poolapi', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f('uq_poolapi_name'), ['name']
        )

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f('uq_user_login'), ['login']
        )

    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.create_unique_constraint(
            batch_op.f('uq_wallet_name'), ['name']
        )
        batch_op.create_foreign_key(
            batch_op.f('fk_wallet_user_id_user'), 'user', ['user_id'], ['id']
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wallet', schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f('fk_wallet_user_id_user'), type_='foreignkey'
        )
        batch_op.drop_constraint(batch_op.f('uq_wallet_name'), type_='unique')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_user_login'), type_='unique')

    with op.batch_alter_table('poolapi', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('uq_poolapi_name'), type_='unique')

    with op.batch_alter_table('currency', schema=None) as batch_op:
        batch_op.drop_constraint(
            batch_op.f('uq_currency_symbol'), type_='unique'
        )
        batch_op.drop_constraint(
            batch_op.f('uq_currency_name'), type_='unique'
        )

    # ### end Alembic commands ###
