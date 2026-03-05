"""Add document_chunks table for chatbot RAG

Revision ID: a3f7c2d1e845
Revises: 016de952e744
Create Date: 2026-03-05

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a3f7c2d1e845'
down_revision: Union[str, Sequence[str], None] = '016de952e744'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create base table with float8[] embedding column
    # (uses native PostgreSQL arrays instead of pgvector for Railway compatibility)
    op.create_table('document_chunks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source', sa.String(), nullable=False, comment='Source file path'),
        sa.Column('chunk_text', sa.Text(), nullable=False, comment='Chunk content'),
        sa.Column('metadata', postgresql.JSONB(), nullable=True, comment='Chunk metadata (section, position)'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add embedding column as float8 array (384 dimensions for all-MiniLM-L6-v2)
    op.execute("ALTER TABLE document_chunks ADD COLUMN embedding float8[] NOT NULL")

    # Create cosine similarity function for vector search
    op.execute("""
        CREATE OR REPLACE FUNCTION cosine_similarity(a float8[], b float8[])
        RETURNS float8 AS $$
            SELECT COALESCE(
                SUM(a_val * b_val) / NULLIF(
                    SQRT(SUM(a_val * a_val)) * SQRT(SUM(b_val * b_val)), 0
                ), 0
            )
            FROM UNNEST(a, b) AS t(a_val, b_val);
        $$ LANGUAGE sql IMMUTABLE
    """)


def downgrade() -> None:
    op.drop_table('document_chunks')
    op.execute("DROP FUNCTION IF EXISTS cosine_similarity(float8[], float8[])")
