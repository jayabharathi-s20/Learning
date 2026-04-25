from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()
db_user=os.getenv("db_user")
db_pw=os.getenv("db_pw")
db_host=os.getenv("db_host")
db_port=os.getenv("db_port")
db_name=os.getenv("db_name")

database_url=f"postgresql://{db_user}:{db_pw}@{db_host}:{db_port}/{db_name}"
engine=create_engine(database_url)

session_creation=sessionmaker(autoflush=False,autocommit=False,bind=engine)
Base=declarative_base()

