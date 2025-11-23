
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from src.blueprints.product import crud, schema
from src.database import SessionLocal
from werkzeug.local import LocalProxy
from flask import g, current_app

product_bp = Blueprint("product", __name__)

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@product_bp.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@product_bp.route("/products/", methods=["POST"])
def create_product():
    db = get_db()
    product = schema.ProductCreate(**request.json)
    return jsonify(crud.create_product(db=db, product=product))


@product_bp.route("/products/", methods=["GET"])
def read_products():
    db = get_db()
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    products = crud.get_products(db, skip=skip, limit=limit)
    return jsonify(products)


@product_bp.route("/products/<int:product_id>", methods=["GET"])
def read_product(product_id: int):
    db = get_db()
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        return jsonify({"detail": "Product not found"}), 404
    return jsonify(db_product)
