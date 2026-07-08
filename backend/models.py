from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.dialects.postgresql import JSON 


#create db model 
class Prisoner(Base):
  __tablename__ = "prisoners"
  id = Column(Integer, primary_key=True, index=True)
  full_name = Column(String, nullable=False)
  age = Column(Integer, nullable=False)
  gender = Column(String, nullable=False)
  description = Column(String, nullable=False)
  last_seen_location = Column(String, nullable=False)
  image_path = Column(String, nullable=False)