from typing import List

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, and_

from database import engine
from models import InSchema, OutSchema

session = Session(bind=engine)

app = FastAPI()
origin = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origin,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.post("/product", response_model=InSchema, status_code=status.HTTP_200_OK, tags=['Store Product'])
#     both function work same
# def product(data: OutSchema, db: Session = Depends(get_db)):
def product(data: OutSchema):
    product_data = InSchema(**data.dict())
    session.add(product_data)
    session.commit()
    session.refresh(product_data)

    # db.add(product_data)
    # db.commit()
    # db.refresh(product_data)

    return product_data


# Get all product
@app.get("/product", response_model=List[InSchema], tags=['Get all Product'])
def get():
    result = session.exec(select(InSchema)).all()
    return result


# Get product with query parameter
@app.get("/products", tags=['Get Product with Query'])
def get(limit: int = 3, skip: int = 2):
    result = session.exec(select(InSchema).limit(limit).offset(skip)).all()
    return result


# get single product:
@app.get("/product/{ID}", tags=['Single Product'], response_model=OutSchema)
def update(ID: int):
    update_query = session.exec(select(InSchema).where(InSchema.id == ID)).first()
    if update_query:
        return update_query
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Product with id {ID} is not present")


@app.put("/product/{ID}", response_model=OutSchema, tags=['Upadate Product'])
def update_data(ID: int, data: OutSchema):
    update = session.exec(select(InSchema).where(InSchema.id == ID)).first()
    print("id", update)
    if update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Product with id {ID} is not present")
    else:
        update.name = data.name
        update.price = data.price
        update.quantity = data.quantity
        session.commit()
        session.refresh(update)
        return update


@app.delete("/product/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Delete Product'], )
def delete_product(id: int):
    data = session.exec(select(InSchema).where(InSchema.id == id)).one_or_none()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your Product with id {id} is not present")
    else:
        session.delete(data)
        session.commit()
        return {"message": "Your post has been successfully deleted"}


@app.get("/name/{name}/quantity/{quantity}", tags=['Single Quantity'], response_model=OutSchema)
def update(name: str, quantity: int):
    update_query = session.exec(
        select(InSchema).where(and_(InSchema.name == name, InSchema.quantity >= quantity))).first()
    print("quantity: ", update_query.quantity >= quantity)
    if update_query:
        update_query.quantity -= quantity
        session.commit()
        return update_query
    elif session.exec(select(InSchema).where(InSchema.name == name)).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Quantity don,t match")
    elif session.exec(select(InSchema).where(InSchema.quantity == quantity)).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product with name {name} is not present")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Your Product with name {name} and quantity {quantity} is not present")
