from sqlmodel import create_engine, Session

DATABASE_NAME = "./order.db"
DATABASE_URL = f"sqlite:///{DATABASE_NAME}"
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = Session(bind=engine)


def get_db():
    db = SessionLocal
    try:
        yield db
    finally:
        db.close()
