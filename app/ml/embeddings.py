import numpy as np
from ..database import Embedding, SessionLocal
from sqlalchemy import text

def store_embedding(text, embedding_vector):
    """
    Store text embedding in PostgreSQL
    """
    db = SessionLocal()
    embedding = Embedding(
        text=text,
        embedding=embedding_vector
    )
    db.add(embedding)
    db.commit()
    db.close()

def search_similar_embeddings(query_vector, limit=5):
    """
    Search for similar embeddings using cosine similarity
    """
    db = SessionLocal()
    result = db.execute(
        text("""
        SELECT text, embedding <=> :query_vector as distance
        FROM embeddings
        ORDER BY embeddings.embedding <=> :query_vector
        LIMIT :limit
        """),
        {"query_vector": query_vector, "limit": limit}
    )
    similar_items = [(row.text, row.distance) for row in result]
    db.close()
    return similar_items
