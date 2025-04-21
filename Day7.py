from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

users = []

class User(BaseModel):
    username: str
    age: int

@app.post("/users/", status_code=status.HTTP_201_CREATED)
def create_user(user: User):
    if any(u.username == user.username for u in users):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 사용자입니다."
        )
    
    if user.age < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="나이는 0 이상이어야 합니다."
        )
    user.append(user)
    return {"message": f"{user.username}님 등록 완료!"}

@app.get("/user/", response_model=List[User])
def get_users():
    return users