from routers import post
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from database import get_session
from models import Post, User
from crud import create_post, get_posts

router = APIRouter()

@router.get("/users/{user_id}/posts", response_model=list[Post])
def get_posts_by_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    statement = select(Post).exec(statement).all()
    posts = session.exec(statement).all()
    return posts

@router.get("/users/{user_id}/posts", response_model=list[Post])
def get_posts_by_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="해당 사용자를 찾을 수 없습니다.")
    statement = select(Post).where(Post.user_id == user_id)
    posts = session.exec(statement).all()
    return posts

@router.get("/posts/{post_id}", response_model=Post)
def get_post_detail(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
    return post