"""SqlAlchemy engine creating"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


os.chdir('..')
os.chdir('./config_files')


with open('mysql_connect') as f:
    connection_str = f.readline().strip()


engine = create_engine(connection_str, echo=True)


Session = sessionmaker(bind=engine)
session = Session()