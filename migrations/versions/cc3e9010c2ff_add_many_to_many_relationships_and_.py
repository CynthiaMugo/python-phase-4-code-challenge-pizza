"""Add many to many relationships and serialize

Revision ID: cc3e9010c2ff
Revises: 90a7ed781129
Create Date: 2025-09-21 15:26:52.080489

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc3e9010c2ff'
down_revision = '90a7ed781129'
branch_labels = None
depends_on = None


def upgrade():
    # Use batch mode for SQLite
    with op.batch_alter_table("restaurant_pizzas") as batch_op:
        batch_op.add_column(sa.Column('pizza_id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('restaurant_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(
            "fk_restaurant_pizzas_pizza_id_pizzas",
            "pizzas",
            ["pizza_id"],
            ["id"],
            ondelete="CASCADE"
        )
        batch_op.create_foreign_key(
            "fk_restaurant_pizzas_restaurant_id_restaurants",
            "restaurants",
            ["restaurant_id"],
            ["id"],
            ondelete="CASCADE"
        )


def downgrade():
    with op.batch_alter_table("restaurant_pizzas") as batch_op:
        batch_op.drop_constraint("fk_restaurant_pizzas_restaurant_id_restaurants", type_="foreignkey")
        batch_op.drop_constraint("fk_restaurant_pizzas_pizza_id_pizzas", type_="foreignkey")
        batch_op.drop_column("restaurant_id")
        batch_op.drop_column("pizza_id")
