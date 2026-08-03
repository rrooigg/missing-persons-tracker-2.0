from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

#create db model 
class Institution(Base):
  __tablename__ = "institutions"
  id = Column(Integer, primary_key=True, index=True)
  name = Column(String, nullable=False, unique=True)
  institution_type=Column(String, nullable=False)
  location=Column(String, nullable=False)
  contact=Column(String, nullable=True)
  people = relationship(
    "Person",
    back_populates="institution",
    cascade="all, delete-orphan"
  )

class Person(Base):
  __tablename__ = "persons"
  id=Column(Integer, primary_key=True, index=True)
  full_name=Column(String, nullable=False)
  age=Column(Integer, nullable=False)
  gender=Column(String, nullable=False)
  description=Column(String, nullable=False)
  last_seen_location=Column(String, nullable=False)
  image_path=Column(String, nullable=False)
  institution_id=Column(
    Integer,
    ForeignKey("institution.id"),
    nullable=False
  )
  institution=relationship(
    "Institution",
    back_populates="people"
  )