from sqlmodel import SQLModel
import models
from database import engine


# without model it does,t create any database and table


# The SQLModel class has a metadata attribute. It is an instance of a class MetaData.
# Whenever you create a class that inherits from SQLModel and is configured with table = True,
# it is registered in this metadata attribute.

def create_db_table():
    SQLModel.metadata.create_all(engine)


# The main purpose of the __name__ == "__main__" is to have some code that is executed
# when your file is called with:
# also called main block


if __name__ == "__main__":
    create_db_table()
