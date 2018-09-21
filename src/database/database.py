from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import sessionmaker

with open("../postgres_info", 'r') as postgres_info:
    user = postgres_info.readline().replace('\n', '')
    password = postgres_info.readline().replace('\n','')
    host = postgres_info.readline().replace('\n', '')
    port = postgres_info.readline().replace('\n', '')
    dbname = postgres_info.readline().replace('\n', '')

db_string = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(user, password, host, port,
                                                                  dbname)

db = create_engine(db_string)
base = declarative_base()


class Enlist(base):
    __table_name__ = 'enlists'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    army_serial_number = Column(String)
    year_of_birth = Column(Integer)
    nativity = Column(String)
    race = Column(String)
    citizenship = Column(String)
    education = Column(String)
    civilian_occupation = Column(String)
    marital_status = Column(String)
    residence_state = Column(String)
    residence_county = Column(String)
    place_of_enlistment = Column(String)
    term_of_enlistment = Column(String)
    longevity = Column(String)
    source_of_army_personnel = Column(String)
    box_number = Column(Integer)
    film_reel_number = Column(Integer)
    field_use_as_desired = Column(String)
    date_of_enlistment = Column(Date)
    branch_alpha_designation = Column(String)
    grade_alpha_designation = Column(String)
    grade_code = Column(String)
    branch_code = Column(String)
    component_of_army = Column(String)
    card_number = Column(Integer)


Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)


class Database():
    def __init__(self):
        pass

    def add(self, row: Enlist):
        pass
