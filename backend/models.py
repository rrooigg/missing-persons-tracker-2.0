from sqlalchemy import Column, Integer, String
from database import Base

class Prisoner(Base):
    __tablename__ = "prisoners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    image_path = Column(String, nullable=False)