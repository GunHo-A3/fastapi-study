from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    quantity: int

@app.post("/items/")
def create_item(item: Item):
    total = item.price * item.quantity
    return{
        "name": item.name,
        "total_price": total
    }