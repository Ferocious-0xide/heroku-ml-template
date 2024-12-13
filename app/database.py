from sqlalchemy import create_engine, Column, Integer, LargeBinary, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class MLModel(Base):
    __tablename__ = "ml_models"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    version = Column(String)
    model_data = Column(LargeBinary)
    
class Embedding(Base):
    __tablename__ = "embeddings"
    
    id = Column(Integer, primary_key=True)
    text = Column(String)
    embedding = Column(Float(array_dimensions=(384,)))
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
