from sqlalchemy import Column, Integer, String, Text
from pgvector.sqlalchemy import Vector
from database import Base

class Prisoner(Base):
  __tablename__ = "prisoners"

  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String, nullable=False)
  age = Column(Integer)
  gender = Column(String)
  description = Column(Text)
  last_seen_location = Column(String)
  image_path = Column(String)
  
  # Facenet produces a 128-float vector
  embedding = Column(Vector(128))