from sqlmodel import Session, select
from models import User, Post

def get_user_by_username(session: Session, username: str):
    return session.exec(select(User).where(User.username == username)).first()

def create_user(session: Session, user: User):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_post(session: Session, post: Post):
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_posts(session: Session):
    return session.exec(select(Post)).all()
