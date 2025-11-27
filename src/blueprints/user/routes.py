
from flask import (
    Blueprint, request, jsonify, render_template, redirect, url_for, flash, session
)
from werkzeug.security import check_password_hash
import pyotp
import qrcode
import io
from base64 import b64encode

from src.blueprints.user import crud, schema
from src.database import SessionLocal
from werkzeug.local import LocalProxy
from flask import g

user_bp = Blueprint("user", __name__)

def get_db():
    if 'db' not in g:
        g.db = SessionLocal()
    return g.db

@user_bp.teardown_request
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# HTML Routes
@user_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        db = get_db()
        email = request.form['email']
        password = request.form['password']
        error = None
        user = crud.get_user_by_email(db, email=email)

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user.hashed_password, password):
            error = 'Incorrect password.'

        if error is None:
            session['user_id_2fa'] = user.id  # Temporary session for 2FA
            return redirect(url_for('user.verify_2fa'))

        flash(error, 'danger')

    return render_template('auth/login.html')

@user_bp.route('/verify-2fa', methods=('GET', 'POST'))
def verify_2fa():
    user_id = session.get('user_id_2fa')
    if not user_id:
        return redirect(url_for('user.login'))

    if request.method == 'POST':
        db = get_db()
        user = crud.get_user(db, user_id)
        token = request.form['token']
        totp = pyotp.TOTP(user.totp_secret)

        if totp.verify(token):
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            # Mark user as verified if you have such a field
            # user.is_verified = True
            # db.commit()
            flash('Login successful!', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid 2FA token.', 'danger')

    return render_template('auth/verify_2fa.html')


@user_bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        db = get_db()
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'
        
        if crud.get_user_by_email(db, email=email):
            error = f"User with email {email} is already registered."

        if error is None:
            user_in = schema.UserCreate(email=email, password=password, username=username)
            user = crud.create_user(db=db, user=user_in)

            # Generate TOTP URI and QR code
            totp_uri = pyotp.totp.TOTP(user.totp_secret).provisioning_uri(
                name=user.email, issuer_name="ApiFood"
            )
            
            # For the user, you would render this in a template
            print(f"TOTP URI: {totp_uri}") # Log to console
            
            # Generate QR code and pass to template
            img = qrcode.make(totp_uri)
            buf = io.BytesIO()
            img.save(buf)
            buf.seek(0)
            qr_code_b64 = b64encode(buf.read()).decode('utf-8')

            flash('You have successfully registered! Please scan the QR code and complete 2FA.', 'success')
            return render_template('auth/register_2fa.html', qr_code=qr_code_b64)

        flash(error, 'danger')

    return render_template('auth/register_email.html')


@user_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.index'))


# API Routes (Keeping them as they are for now)
@user_bp.route("/users/", methods=["POST"])
def create_user_api():
    db = get_db()
    try:
        user = schema.UserCreate(**request.json)
    except TypeError:
        return jsonify({"detail": "Invalid JSON"}), 400

    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return jsonify({"detail": "Email already registered"}), 400
    
    created_user = crud.create_user(db=db, user=user)
    return jsonify(schema.User.from_orm(created_user).dict())


@user_bp.route("/users/", methods=["GET"])
def read_users():
    db = get_db()
    skip = request.args.get('skip', 0, type=int)
    limit = request.args.get('limit', 100, type=int)
    users = crud.get_users(db, skip=skip, limit=limit)
    return jsonify([schema.User.from_orm(u).dict() for u in users])


@user_bp.route("/users/<int:user_id>", methods=["GET"])
def read_user(user_id: int):
    db = get_db()
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        return jsonify({"detail": "User not found"}), 404
    return jsonify(schema.User.from_orm(db_user).dict())
