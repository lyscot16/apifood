
import pyotp
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from src.blueprints.user import schema
from src.models.user import User

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schema.UserCreate):
    hashed_password = generate_password_hash(user.password)
    totp_secret = pyotp.random_base32()
    db_user = User(
        email=user.email, 
        hashed_password=hashed_password, 
        username=user.username, 
        totp_secret=totp_secret
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
