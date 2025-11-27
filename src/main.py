
import json
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()

def create_app():

    app = Flask(__name__,
                instance_path=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'instance')),
                instance_relative_config=True,
                template_folder='./templates',
                static_folder='./static'
    )

    # Corrected path for secret.json
    secret_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'secret.json'))
    app.config.from_file(secret_path, load=json.load)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from src.models.user import User
        return User.query.get(int(user_id))
    
    db.init_app(app)

    from src.blueprints.main.routes import main_blueprint
    from src.blueprints.user.routes import user_bp
    from src.blueprints.company.routes import company_bp
    from src.blueprints.product.routes import product_bp
    from src.blueprints.promotion.routes import promotion_bp


    app.register_blueprint(main_blueprint)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(company_bp, url_prefix='/company')
    app.register_blueprint(product_bp, url_prefix='/product')
    app.register_blueprint(promotion_bp, url_prefix='/promotion')


    return app
