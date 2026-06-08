#setup a connection between python & postgresql
from sqlalchemy import create_engine   #core object to communicate with database
from sqlalchemy.ext.declarative import declarative_base  #creates a base class which db models will inherit from
from sqlalchemy.orm import sessionmaker   #session like a 'conversation' with the db i.e crud operations with db
#database url
DATABASE_URL = "postgresql://postgres:Abdigani04@localhost/prisoners"

#create engine -> create 1 engine for whole application(manages connections, sends sql queries, talk to postresql)
engine = create_engine(DATABASE_URL)

#create sessions
SessionLocal = sessionmaker(
  autocommit=False, #changes aren't automatically saved
  autoflush=False, #will not push pending changes before queries
  bind=engine #connects session to engine created
)

#Base class for models
Base = declarative_base()