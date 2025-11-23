
from sqlalchemy.orm import Session

from src.blueprints.promotion import schema
from src.models.promotion import Promotion


def get_promotion(db: Session, promotion_id: int):
    return db.query(Promotion).filter(Promotion.id == promotion_id).first()


def get_promotions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Promotion).offset(skip).limit(limit).all()


def create_promotion(db: Session, promotion: schema.PromotionCreate):
    db_promotion = Promotion(**promotion.dict())
    db.add(db_promotion)
    db.commit()
    db.refresh(db_promotion)
    return db_promotion
