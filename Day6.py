from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []


class User(BaseModel):
    username: str
    age: int 

@app.post("/users/")
def create_user(user: User):
    users.append(user)
    return {"message": f"{user.username}님 등록 완료!"}

@app.get("/users/", response_model=List[User])
def get_user():
    return users