from pydantic import BaseModel
from datetime import datetime


class PromotionBase(BaseModel):
    discount_percentage: float
    end_date: datetime


class PromotionCreate(PromotionBase):
    pass


class Promotion(PromotionBase):
    id: int
    product_id: int

    class Config:
        from_attributes = True
