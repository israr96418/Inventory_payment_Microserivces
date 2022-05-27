import httpx
from fastapi import FastAPI, status, HTTPException
from sqlmodel import Session

from database import engine
from models import Product

app = FastAPI()

session = Session(bind=engine)


# url = 'http://127.0.0.1:8000/product/'
# data = os.environ.get('url')


@app.get("/")
def Get_all_product():
    with httpx.Client() as client:
        r = client.get('http://127.0.0.1:8000/product')
        print(r.text)
        return r.json()


@app.get("/{ID}")
def Get_all_product(ID: int):
    r = httpx.get(f'http://127.0.0.1:8000/product/{ID}')
    a = r.json()
    return a


@app.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
def Buy_Product(data: Product):
    with httpx.Client() as client:
        r = client.get(f'http://127.0.0.1:8000/name/{data.name}/quantity/{data.quantity}')
        print("status code from inventory: ", r.status_code)
        if r.status_code == 200:
            productivity = Product(**data.dict())
            session.add(productivity)
            session.commit()
            session.refresh(productivity)
            return productivity
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Your product name {data.name} or quantity {data.quantity} don,t match")
