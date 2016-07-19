"""empty message

Revision ID: a4f17e7db43b
Revises: None
Create Date: 2016-07-19 14:15:25.508645

"""

# revision identifiers, used by Alembic.
revision = 'a4f17e7db43b'
down_revision = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('address_line', sa.String(), nullable=False),
    sa.Column('suburb', sa.String(), nullable=False),
    sa.Column('state', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(length=8), nullable=False),
    sa.Column('country', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('audit_event',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('type', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user', sa.String(), nullable=True),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('object_type', sa.String(), nullable=True),
    sa.Column('object_id', sa.BigInteger(), nullable=True),
    sa.Column('acknowledged', sa.Boolean(), nullable=False),
    sa.Column('acknowledged_by', sa.String(), nullable=True),
    sa.Column('acknowledged_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_audit_events_object_and_type', 'audit_event', ['object_type', 'object_id', 'type', 'created_at'], unique=False)
    op.create_index('idx_audit_events_type_acknowledged', 'audit_event', ['type', 'acknowledged'], unique=False)
    op.create_index(op.f('ix_audit_event_acknowledged'), 'audit_event', ['acknowledged'], unique=False)
    op.create_index(op.f('ix_audit_event_created_at'), 'audit_event', ['created_at'], unique=False)
    op.create_index(op.f('ix_audit_event_type'), 'audit_event', ['type'], unique=False)
    op.create_table('contact',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('contact_for', sa.String(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.Column('fax', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('framework',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('framework', sa.String(), nullable=False),
    sa.Column('framework_agreement_version', sa.String(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('clarification_questions_open', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_framework_framework'), 'framework', ['framework'], unique=False)
    op.create_index(op.f('ix_framework_slug'), 'framework', ['slug'], unique=True)
    op.create_index(op.f('ix_framework_status'), 'framework', ['status'], unique=False)
    op.create_table('lot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('slug', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('one_service_limit', sa.Boolean(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_lot_slug'), 'lot', ['slug'], unique=False)
    op.create_table('service_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('framework_lot',
    sa.Column('framework_id', sa.Integer(), nullable=False),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.PrimaryKeyConstraint('framework_id', 'lot_id')
    )
    op.create_table('supplier',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data_version', sa.Integer(), nullable=True),
    sa.Column('code', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('summary', sa.String(length=511), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('address_id', sa.Integer(), nullable=False),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('abn', sa.String(length=15), nullable=True),
    sa.Column('acn', sa.String(length=15), nullable=True),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_supplier_code'), 'supplier', ['code'], unique=True)
    op.create_table('archived_service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('service_id', sa.String(), nullable=False),
    sa.Column('framework_id', sa.BigInteger(), nullable=False),
    sa.Column('lot_id', sa.BigInteger(), nullable=False),
    sa.Column('supplier_code', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['framework_id', 'lot_id'], ['framework_lot.framework_id', 'framework_lot.lot_id'], ),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_archived_service_framework_id'), 'archived_service', ['framework_id'], unique=False)
    op.create_index(op.f('ix_archived_service_lot_id'), 'archived_service', ['lot_id'], unique=False)
    op.create_index(op.f('ix_archived_service_service_id'), 'archived_service', ['service_id'], unique=False)
    op.create_index(op.f('ix_archived_service_supplier_code'), 'archived_service', ['supplier_code'], unique=False)
    op.create_table('brief',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('framework_id', sa.Integer(), nullable=False),
    sa.Column('lot_id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['framework_id', 'lot_id'], ['framework_lot.framework_id', 'framework_lot.lot_id'], ),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brief_created_at'), 'brief', ['created_at'], unique=False)
    op.create_index(op.f('ix_brief_published_at'), 'brief', ['published_at'], unique=False)
    op.create_index(op.f('ix_brief_updated_at'), 'brief', ['updated_at'], unique=False)
    op.create_table('draft_service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('service_id', sa.String(), nullable=True),
    sa.Column('framework_id', sa.BigInteger(), nullable=False),
    sa.Column('lot_id', sa.BigInteger(), nullable=False),
    sa.Column('supplier_code', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['framework_id', 'lot_id'], ['framework_lot.framework_id', 'framework_lot.lot_id'], ),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_draft_service_framework_id'), 'draft_service', ['framework_id'], unique=False)
    op.create_index(op.f('ix_draft_service_lot_id'), 'draft_service', ['lot_id'], unique=False)
    op.create_index(op.f('ix_draft_service_service_id'), 'draft_service', ['service_id'], unique=False)
    op.create_index(op.f('ix_draft_service_supplier_code'), 'draft_service', ['supplier_code'], unique=False)
    op.create_table('service',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('service_id', sa.String(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=True),
    sa.Column('status', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('framework_id', sa.BigInteger(), nullable=False),
    sa.Column('lot_id', sa.BigInteger(), nullable=False),
    sa.Column('supplier_code', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['framework_id', 'lot_id'], ['framework_lot.framework_id', 'framework_lot.lot_id'], ),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['lot_id'], ['lot.id'], ),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_service_framework_id'), 'service', ['framework_id'], unique=False)
    op.create_index(op.f('ix_service_lot_id'), 'service', ['lot_id'], unique=False)
    op.create_index(op.f('ix_service_service_id'), 'service', ['service_id'], unique=True)
    op.create_index(op.f('ix_service_supplier_code'), 'service', ['supplier_code'], unique=False)
    op.create_table('supplier__contact',
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('contact_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['contact_id'], ['contact.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('supplier_id', 'contact_id')
    )
    op.create_table('supplier__service_category',
    sa.Column('supplier_id', sa.Integer(), nullable=False),
    sa.Column('service_category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['service_category_id'], ['service_category.id'], ),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('supplier_id', 'service_category_id')
    )
    op.create_table('supplier_framework',
    sa.Column('supplier_code', sa.BigInteger(), nullable=False),
    sa.Column('framework_id', sa.Integer(), nullable=False),
    sa.Column('declaration', postgresql.JSON(), nullable=True),
    sa.Column('on_framework', sa.Boolean(), nullable=True),
    sa.Column('agreement_returned_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['framework_id'], ['framework.id'], ),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('supplier_code', 'framework_id')
    )
    op.create_table('supplier_reference',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('supplier_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('organisation', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['supplier_id'], ['supplier.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('email_address', sa.String(), nullable=False),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.Column('password_changed_at', sa.DateTime(), nullable=False),
    sa.Column('logged_in_at', sa.DateTime(), nullable=True),
    sa.Column('failed_login_count', sa.Integer(), nullable=False),
    sa.Column('role', sa.Enum('buyer', 'supplier', 'admin', 'admin-ccs-category', 'admin-ccs-sourcing', name='user_roles_enum'), nullable=False),
    sa.Column('supplier_code', sa.BigInteger(), nullable=True),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email_address'), 'user', ['email_address'], unique=True)
    op.create_index(op.f('ix_user_supplier_code'), 'user', ['supplier_code'], unique=False)
    op.create_table('brief_clarification_question',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brief_id', sa.Integer(), nullable=False),
    sa.Column('question', sa.String(), nullable=False),
    sa.Column('answer', sa.String(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['brief_id'], ['brief.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brief_clarification_question_published_at'), 'brief_clarification_question', ['published_at'], unique=False)
    op.create_table('brief_response',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('data', postgresql.JSON(), nullable=False),
    sa.Column('brief_id', sa.Integer(), nullable=False),
    sa.Column('supplier_code', sa.BigInteger(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['brief_id'], ['brief.id'], ),
    sa.ForeignKeyConstraint(['supplier_code'], ['supplier.code'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_brief_response_created_at'), 'brief_response', ['created_at'], unique=False)
    op.create_table('brief_user',
    sa.Column('brief_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['brief_id'], ['brief.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('brief_id', 'user_id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('brief_user')
    op.drop_index(op.f('ix_brief_response_created_at'), table_name='brief_response')
    op.drop_table('brief_response')
    op.drop_index(op.f('ix_brief_clarification_question_published_at'), table_name='brief_clarification_question')
    op.drop_table('brief_clarification_question')
    op.drop_index(op.f('ix_user_supplier_code'), table_name='user')
    op.drop_index(op.f('ix_user_email_address'), table_name='user')
    op.drop_table('user')
    op.drop_table('supplier_reference')
    op.drop_table('supplier_framework')
    op.drop_table('supplier__service_category')
    op.drop_table('supplier__contact')
    op.drop_index(op.f('ix_service_supplier_code'), table_name='service')
    op.drop_index(op.f('ix_service_service_id'), table_name='service')
    op.drop_index(op.f('ix_service_lot_id'), table_name='service')
    op.drop_index(op.f('ix_service_framework_id'), table_name='service')
    op.drop_table('service')
    op.drop_index(op.f('ix_draft_service_supplier_code'), table_name='draft_service')
    op.drop_index(op.f('ix_draft_service_service_id'), table_name='draft_service')
    op.drop_index(op.f('ix_draft_service_lot_id'), table_name='draft_service')
    op.drop_index(op.f('ix_draft_service_framework_id'), table_name='draft_service')
    op.drop_table('draft_service')
    op.drop_index(op.f('ix_brief_updated_at'), table_name='brief')
    op.drop_index(op.f('ix_brief_published_at'), table_name='brief')
    op.drop_index(op.f('ix_brief_created_at'), table_name='brief')
    op.drop_table('brief')
    op.drop_index(op.f('ix_archived_service_supplier_code'), table_name='archived_service')
    op.drop_index(op.f('ix_archived_service_service_id'), table_name='archived_service')
    op.drop_index(op.f('ix_archived_service_lot_id'), table_name='archived_service')
    op.drop_index(op.f('ix_archived_service_framework_id'), table_name='archived_service')
    op.drop_table('archived_service')
    op.drop_index(op.f('ix_supplier_code'), table_name='supplier')
    op.drop_table('supplier')
    op.drop_table('framework_lot')
    op.drop_table('service_category')
    op.drop_index(op.f('ix_lot_slug'), table_name='lot')
    op.drop_table('lot')
    op.drop_index(op.f('ix_framework_status'), table_name='framework')
    op.drop_index(op.f('ix_framework_slug'), table_name='framework')
    op.drop_index(op.f('ix_framework_framework'), table_name='framework')
    op.drop_table('framework')
    op.drop_table('contact')
    op.drop_index(op.f('ix_audit_event_type'), table_name='audit_event')
    op.drop_index(op.f('ix_audit_event_created_at'), table_name='audit_event')
    op.drop_index(op.f('ix_audit_event_acknowledged'), table_name='audit_event')
    op.drop_index('idx_audit_events_type_acknowledged', table_name='audit_event')
    op.drop_index('idx_audit_events_object_and_type', table_name='audit_event')
    op.drop_table('audit_event')
    op.drop_table('address')
    ### end Alembic commands ###
