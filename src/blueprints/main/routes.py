from flask import Blueprint, render_template
from src.models.company import Company
from src.database import SessionLocal

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    db = SessionLocal()
    companies = db.query(Company).all()
    db.close()
    return render_template('index.html', companies=companies)
