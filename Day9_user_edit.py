from fastapi import FastAPI, HTTPException
from sqlmodel import Field, SQLModel, Session, create_engine, select
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    age: int
    city: str

sqlite_file_name = "users.db"
engine = create_engine(f'sqlite:///{sqlite_file_name}', echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db

@app.post("/users/", response_model=User)
def create_user(user: User):
    with Session(engine) as session:
        exists = session.exec(select(User).where(User.username == user.username)).first()
        if exists:
            raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.get("/users/", response_model=List[User])
def read_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users

@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, new_data: User):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        user.username = new_data.username
        user.age = new_data.age
        user.city = new_data.city
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    with Session(engine) as session:
        user = session.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
        session.delete(user)
        session.commit()
        return {"message": f"{user.username}님 삭제 완료"}