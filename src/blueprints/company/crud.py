
from sqlalchemy.orm import Session

from src.blueprints.company import schema
from src.models.company import Company
from src.models.product import Product


def get_company(db: Session, company_id: int):
    return db.query(Company).filter(Company.id == company_id).first()


def get_company_by_name(db: Session, name: str):
    return db.query(Company).filter(Company.name == name).first()


def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Company).offset(skip).limit(limit).all()


def create_company(db: Session, company: schema.CompanyCreate):
    db_company = Company(name=company.name, description=company.description)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_company_products(db: Session, company_id: int, skip: int = 0, limit: int = 100):
    return db.query(Product).filter(Product.company_id == company_id).offset(skip).limit(limit).all()
