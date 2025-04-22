from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import Optional, List

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    age: int
    city: str

sqlite_file_name = "users.db"
engine = create_engine(f"sqlite:///{sqlite_file_name}", echo=True)

def create_db():
    SQLModel.metadata.create_all(engine)

app =FastAPI()

@app.on_event("startup")
def on_startup():
    create_db()

@app.post("/users/")
def create_user(user: User):
    with Session(engine) as session:
        statement = select(User).where(User.username == user.username)
        result = session.exec(statement).first()
        if result:
            raise HTTPException(status_code=400, detail="이미 존재하는 사람입니다.")
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
@app.get("/users/", response_model=List[User])
def get_users():
    with Session(engine) as session:
        statement = select(User)
        result = session.exec(statement).all()
        return result