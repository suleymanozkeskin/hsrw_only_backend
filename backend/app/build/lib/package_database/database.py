 # ORM => OBJECT RELATIONAL MAPPING



from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


## CONNECTION FORMAT BELOW: 
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip-address>/<hostname>/<database_name>"

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost/fastapi"

## create engine:

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
