
from flask import Flask
import json
import os
from src.database import engine, Base
from src.models import company, product, promotion, user

def create_app():
    Base.metadata.create_all(bind=engine)
    app = Flask(__name__)

    # Load secret key from instance/secret.json
    instance_path = os.path.join(app.root_path, 'instance')
    secret_file_path = os.path.join(instance_path, 'secret.json')

    if os.path.exists(secret_file_path):
        with open(secret_file_path, 'r') as f:
            secrets = json.load(f)
            app.config['SECRET_KEY'] = secrets.get('SECRET_KEY')
    else:
        # Fallback or error handling if secret.json is not found
        # In a real application, you might want to raise an error or log a warning
        app.config['SECRET_KEY'] = 'a_fallback_secret_key_you_should_never_use_in_prod'

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
