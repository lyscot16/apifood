
from flask import Flask
from src.database import engine, Base
from src.models import company, product, promotion, user

def create_app():
    Base.metadata.create_all(bind=engine)
    app = Flask(__name__)

    from src.blueprints.company.routes import company_bp
    from src.blueprints.product.routes import product_bp
    from src.blueprints.promotion.routes import promotion_bp
    from src.blueprints.user.routes import user_bp
    from src.blueprints.main.routes import main_bp

    app.register_blueprint(company_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(promotion_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)

    return app
