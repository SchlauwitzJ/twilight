import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database
from twilight.Item.Tabulars import Base
from sqlalchemy.orm import sessionmaker


def create_or_access_db(user, password, address, db_name, echo=True, reset=False):
    print(sqlalchemy.__version__)
    url = f"mysql+pymysql://{user}:{password}@{address}/{db_name}"

    engine = create_engine(url=url, echo=echo)

    if database_exists(engine.url) and reset:
        print(f"{db_name} was reset.")
        drop_database(engine.url)
    if not database_exists(engine.url):
        print(f"Creating {db_name}.")
        create_database(engine.url)
    else:
        engine.connect()
    print("Connected...")
    Base.metadata.create_all(engine)

    sess = sessionmaker()
    sess.configure(bind=engine)
    print(f"Session started for {user} in {db_name}.")
    return sess()
