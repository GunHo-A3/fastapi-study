from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Field, SQLModel, Session, create_engine, select, Relationship
from typing import Optional, List

sqlite_file_name = "relational.db"
engine = create_engine(f'sqlite:///{sqlite_file_name}', echo=False)

def get_session():
    with Session(engine) as session:
        yield session

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str   # ✅ 이렇게 타입 힌트 붙여야 함
    age: int
    city: str
    posts: List[Post] = Relationship(back_populates="user")

Post.user = Relationship(back_populates="posts")

app = FastAPI()

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/user/")
def create_user(user: User, session: Session = Depends(get_session)):
    exists = session.exec(select(User).where(User.username == user.username)).first()
    if exists:
        raise HTTPException(status_code=400, detail="이미 존재하는 사용자입니다.")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@app.post("/post/")
def create_post(post: Post, session: Session = Depends(get_session)):
    user = session.get(User, post.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="작성자(id) 없음")
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

@app.get("/post/", response_model=List[Post])
def get_posts(session: Session = Depends(get_session)):
    return session.exec(select(Post)).all()
