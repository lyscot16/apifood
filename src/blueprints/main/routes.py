
from flask import render_template, Blueprint
from flask_login import current_user
from ...models.company import Company

main_blueprint = Blueprint('main', __name__)

@main_blueprint.route('/')
def index():
    companies = Company.query.all()
    return render_template(
        'index.html', 
        companies=companies, 
        current_user=current_user
    )
