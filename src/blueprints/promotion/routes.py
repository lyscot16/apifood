
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session

from src.blueprints.promotion import crud, schema
from src.database import SessionLocal
from werkzeug.local import LocalProxy
from flask import g, current_app

promotion_bp = Blueprint("promotion", __name__)

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@promotion_bp.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)

    if db is not None:
        db.close()


@promotion_bp.route("/promotions/", methods=["POST"])
def create_promotion():
    db = get_db()
    promotion = schema.PromotionCreate(**request.json)
    return jsonify(crud.create_promotion(db=db, promotion=promotion))


@promotion_bp.route("/promotions/", methods=["GET"])
def read_promotions():
    db = get_db()
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    promotions = crud.get_promotions(db, skip=skip, limit=limit)
    return jsonify(promotions)


@promotion_bp.route("/promotions/<int:promotion_id>", methods=["GET"])
def read_promotion(promotion_id: int):
    db = get_db()
    db_promotion = crud.get_promotion(db, promotion_id=promotion_id)
    if db_promotion is None:
        return jsonify({"detail": "Promotion not found"}), 404
    return jsonify(db_promotion)
