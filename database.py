from sqlmodel import create_engine, Session


DATABASE_NAME = "./database.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
# DATABASE_URL = "mysql+mysqldb://isrardawar:dawar96418@localhost:3306/inventory"
# You should normally have a single engine object for your whole application and re-use it everywhere
# echo=True. It will make the engine print all the SQL statements it executes, which can help you understand what's happening.
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = Session(bind=engine)


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
