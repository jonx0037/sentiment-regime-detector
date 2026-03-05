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
    # Enable pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create base table
    op.create_table('document_chunks',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source', sa.String(), nullable=False, comment='Source file path'),
        sa.Column('chunk_text', sa.Text(), nullable=False, comment='Chunk content'),
        sa.Column('metadata', postgresql.JSONB(), nullable=True, comment='Chunk metadata (section, position)'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add vector column (pgvector — not supported by SQLAlchemy autogenerate)
    op.execute("ALTER TABLE document_chunks ADD COLUMN embedding vector(384) NOT NULL")

    # Create HNSW index for cosine similarity search
    op.execute("""
        CREATE INDEX document_chunks_embedding_idx
        ON document_chunks USING hnsw (embedding vector_cosine_ops)
    """)


def downgrade() -> None:
    op.drop_table('document_chunks')
