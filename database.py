import oracledb
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIALECT = 'oracle'
SQL_DRIVER = 'oracledb'
USERNAME = 'system'
PASSWORD = 'SysPassword1'
HOST = 'DevServerAlpha'
PORT = 1521
SERVICE_NAME = 'cdb1'

cp = oracledb.ConnectParams()
cp.parse_connect_string(f"{HOST}:{PORT}/{SERVICE_NAME}")
thick_mode = None

engine = create_engine(
    f'oracle+oracledb://{USERNAME}:{PASSWORD}@{cp.host}:{cp.port}/?service_name={cp.service_name}',
    thick_mode=thick_mode)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()