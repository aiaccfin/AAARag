"""initial

Revision ID: ddd1745150eb
Revises: 
Create Date: 2025-12-03 13:34:53.552095

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ddd1745150eb'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('audit_logs',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('role_id', sa.Integer(), nullable=True),
        sa.Column('table_name', sa.String(), nullable=False),
        sa.Column('operation', sa.String(), nullable=False),
        sa.Column('data_before', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('data_after', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_tenant_id'), 'audit_logs', ['tenant_id'], unique=False)

    op.create_table('bankstatements_rls',
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('date', sa.DateTime(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('updated_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bankstatements_rls_category'), 'bankstatements_rls', ['category'], unique=False)
    op.create_index(op.f('ix_bankstatements_rls_tenant_id'), 'bankstatements_rls', ['tenant_id'], unique=False)

    op.create_table('gst62_rlsfff_audit_logs',
        sa.Column('tax_code', sa.String(), nullable=False),
        sa.Column('tax_name', sa.String(), nullable=False),
        sa.Column('tax_rate', sa.Float(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('effective_date', sa.DateTime(), nullable=False),
        sa.Column('tax_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('jurisdiction_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('compliance_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('tenant_id', sa.String(), nullable=False),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_gst62_rlsfff_audit_logs_tax_code'), 'gst62_rlsfff_audit_logs', ['tax_code'], unique=False)
    op.create_index(op.f('ix_gst62_rlsfff_audit_logs_tenant_id'), 'gst62_rlsfff_audit_logs', ['tenant_id'], unique=False)

    op.create_table('person',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('person_type', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('tenants',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('created_by', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('notes', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_name'), 'tenants', ['name'], unique=False)

    op.create_table('parentchild',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('tenant_id', sa.Uuid(), nullable=False),
        sa.Column('parent_id', sa.Uuid(), nullable=False),
        sa.Column('child_id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['person.id']),
        sa.ForeignKeyConstraint(['parent_id'], ['person.id']),
        sa.PrimaryKeyConstraint('id')
    )

    op.drop_index(op.f('ix_user_manager_id'), table_name='user')
    op.drop_table('user')

    op.create_unique_constraint(None, 'invoices_rls', ['tenant_id', 'invoice_sequence'])

    op.add_column('payments_rls', sa.Column('customer_id', sa.Uuid(), nullable=True))
    op.add_column('payments_rls', sa.Column('customer_snapshot', postgresql.JSONB(astext_type=sa.Text()), nullable=True))
    op.add_column('payments_rls', sa.Column('payment_method', sa.String(), nullable=True))
    op.add_column('payments_rls', sa.Column('deposit_account_id', sa.Uuid(), nullable=True))
    op.add_column('payments_rls', sa.Column('reference_no', sa.String(), nullable=True))
    op.add_column('payments_rls', sa.Column('notes', sa.String(), nullable=True))
    op.add_column('payments_rls', sa.Column('amount_received', sa.Float(), nullable=True))
    op.create_index(op.f('ix_payments_rls_customer_id'), 'payments_rls', ['customer_id'], unique=False)

    op.drop_column('tenant_sequences', 'next_receipt_number')

    op.add_column('user_rls', sa.Column('description', sa.String(), nullable=True))


def downgrade() -> None:
    # unchanged from your file (only upgrade needed patch)
    ...
