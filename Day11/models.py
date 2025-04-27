from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int = Field(foreign_key="user.id")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    age: int
    city: str
    posts: List["Post"] = Relationship(back_populates="user")

Post.user = Relationship(back_populates="posts")
