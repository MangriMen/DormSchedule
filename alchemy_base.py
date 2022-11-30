from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from consts import SQLITE_ENGINE_CONNECTION

engine = create_engine(SQLITE_ENGINE_CONNECTION)

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)