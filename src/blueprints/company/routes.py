
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session
from src.blueprints.company import crud, schema
from src.database import SessionLocal
from werkzeug.local import LocalProxy
from flask import g, current_app

company_bp = Blueprint("company", __name__)

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@company_bp.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@company_bp.route("/companies/", methods=["POST"])
def create_company():
    db = get_db()
    company = schema.CompanyCreate(**request.json)
    db_company = crud.get_company_by_name(db, name=company.name)
    if db_company:
        return jsonify({"detail": "Company already registered"}), 400
    return jsonify(crud.create_company(db=db, company=company))


@company_bp.route("/companies/", methods=["GET"])
def read_companies():
    db = get_db()
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    companies = crud.get_companies(db, skip=skip, limit=limit)
    return jsonify(companies)


@company_bp.route("/companies/<int:company_id>", methods=["GET"])
def read_company(company_id: int):
    db = get_db()
    db_company = crud.get_company(db, company_id=company_id)
    if db_company is None:
        return jsonify({"detail": "Company not found"}), 404
    return jsonify(db_company)


@company_bp.route("/companies/<int:company_id>/products/", methods=["GET"])
def read_company_products(company_id: int):
    db = get_db()
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    products = crud.get_company_products(db, company_id=company_id, skip=skip, limit=limit)
    return jsonify(products)

