"""initial

Revision ID: 0001_initial
Revises:
Create Date: 2026-02-28
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'stores',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False),
        sa.Column('slug', sa.String(length=80), nullable=False),
        sa.Column('whatsapp_e164', sa.String(length=20), nullable=False),
        sa.Column('address_text', sa.Text(), nullable=True),
        sa.Column('currency', sa.String(length=3), nullable=False, server_default='NIO'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('slug'),
    )
    op.create_index('idx_stores_active', 'stores', ['is_active'], unique=False)

    op.create_table(
        'store_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('email', sa.String(length=160), nullable=False),
        sa.Column('password_hash', sa.Text(), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.CheckConstraint("role IN ('OWNER','STAFF')", name='ck_store_users_role'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_id', 'email', name='uq_store_users_store_email'),
    )
    op.create_index('idx_store_users_store', 'store_users', ['store_id'], unique=False)

    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=80), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_id', 'name', name='uq_categories_store_name'),
    )
    op.create_index('idx_categories_store', 'categories', ['store_id'], unique=False)

    op.create_table(
        'products',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('category_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name', sa.String(length=140), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('price', sa.Numeric(12, 2), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),
        sa.Column('stock_qty', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['category_id'], ['categories.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.CheckConstraint('price >= 0', name='ck_products_price_nonnegative'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_products_store', 'products', ['store_id'], unique=False)
    op.create_index('idx_products_active', 'products', ['store_id', 'is_active'], unique=False)

    op.create_table(
        'product_images',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('url', sa.Text(), nullable=False),
        sa.Column('sort_order', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_product_images_product', 'product_images', ['product_id'], unique=False)

    op.create_table(
        'customers',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('whatsapp_e164', sa.String(length=20), nullable=False),
        sa.Column('name_last', sa.String(length=140), nullable=True),
        sa.Column('total_orders', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('last_order_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_id', 'whatsapp_e164', name='uq_customer_store_whatsapp'),
    )
    op.create_index('idx_customers_store_whatsapp', 'customers', ['store_id', 'whatsapp_e164'], unique=False)

    op.create_table(
        'orders',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('store_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('customer_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('public_code', sa.String(length=12), nullable=False),
        sa.Column('status', sa.Enum('CREATED', 'CONFIRMED', 'PREPARING', 'SHIPPED', 'DELIVERED', 'CANCELLED', name='orderstatus'), nullable=False),
        sa.Column('customer_name', sa.String(length=140), nullable=False),
        sa.Column('customer_whatsapp', sa.String(length=20), nullable=False),
        sa.Column('address_text', sa.Text(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column('delivery_method', sa.Enum('DELIVERY', 'PICKUP', name='deliverymethod'), nullable=False),
        sa.Column('delivery_fee', sa.Numeric(12, 2), nullable=False, server_default='0'),
        sa.Column('payment_method', sa.Enum('CASH', 'TRANSFER', 'CARD_LINK', name='paymentmethod'), nullable=False),
        sa.Column('subtotal', sa.Numeric(12, 2), nullable=False),
        sa.Column('total', sa.Numeric(12, 2), nullable=False),
        sa.Column('whatsapp_message', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['store_id'], ['stores.id'], ondelete='CASCADE'),
        sa.CheckConstraint('delivery_fee >= 0', name='ck_orders_delivery_fee_nonnegative'),
        sa.CheckConstraint('subtotal >= 0', name='ck_orders_subtotal_nonnegative'),
        sa.CheckConstraint('total >= 0', name='ck_orders_total_nonnegative'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('store_id', 'public_code', name='uq_orders_store_public_code'),
    )
    op.create_index('idx_orders_store_status', 'orders', ['store_id', 'status'], unique=False)
    op.create_index('idx_orders_store_created', 'orders', ['store_id', 'created_at'], unique=False)

    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS trigger AS $$
        BEGIN
          NEW.updated_at = now();
          RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )
    op.execute(
        """
        CREATE TRIGGER trg_orders_updated_at
        BEFORE UPDATE ON orders
        FOR EACH ROW EXECUTE FUNCTION set_updated_at();
        """
    )

    op.create_table(
        'order_items',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('product_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('name_snapshot', sa.String(length=140), nullable=False),
        sa.Column('price_snapshot', sa.Numeric(12, 2), nullable=False),
        sa.Column('qty', sa.Integer(), nullable=False),
        sa.Column('line_total', sa.Numeric(12, 2), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='SET NULL'),
        sa.CheckConstraint('price_snapshot >= 0', name='ck_order_items_price_snapshot_nonnegative'),
        sa.CheckConstraint('qty > 0', name='ck_order_items_qty_positive'),
        sa.CheckConstraint('line_total >= 0', name='ck_order_items_line_total_nonnegative'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_order_items_order', 'order_items', ['order_id'], unique=False)

    op.create_table(
        'payments',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('order_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('method', sa.Enum('CASH', 'TRANSFER', 'CARD_LINK', name='paymentmethod'), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('reference', sa.String(length=120), nullable=True),
        sa.Column('receipt_url', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ondelete='CASCADE'),
        sa.CheckConstraint('amount >= 0', name='ck_payments_amount_nonnegative'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('idx_payments_order', 'payments', ['order_id'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_payments_order', table_name='payments')
    op.drop_table('payments')

    op.drop_index('idx_order_items_order', table_name='order_items')
    op.drop_table('order_items')

    op.execute('DROP TRIGGER IF EXISTS trg_orders_updated_at ON orders;')
    op.execute('DROP FUNCTION IF EXISTS set_updated_at();')

    op.drop_index('idx_orders_store_created', table_name='orders')
    op.drop_index('idx_orders_store_status', table_name='orders')
    op.drop_table('orders')

    op.drop_index('idx_customers_store_whatsapp', table_name='customers')
    op.drop_table('customers')

    op.drop_index('idx_product_images_product', table_name='product_images')
    op.drop_table('product_images')

    op.drop_index('idx_products_active', table_name='products')
    op.drop_index('idx_products_store', table_name='products')
    op.drop_table('products')

    op.drop_index('idx_categories_store', table_name='categories')
    op.drop_table('categories')

    op.drop_index('idx_store_users_store', table_name='store_users')
    op.drop_table('store_users')

    op.drop_index('idx_stores_active', table_name='stores')
    op.drop_table('stores')

    sa.Enum(name='paymentmethod').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='deliverymethod').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='orderstatus').drop(op.get_bind(), checkfirst=False)
