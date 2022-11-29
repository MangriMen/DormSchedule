from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from configs.consts import SQLITE_ENGINE_CONNECTION

engine = create_engine(SQLITE_ENGINE_CONNECTION, echo=False)

Base = declarative_base(bind=engine)
Session = sessionmaker(bind=engine)