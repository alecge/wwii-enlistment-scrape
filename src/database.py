from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base


db_string = "postgres://"

db = create_engine(db_string)
base = declarative_base()