from flask import request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from notlar import app, db
from notlar.models import User
from sqlalchemy.exc import IntegrityError
import re
from flask_login import login_user, login_required, logout_user, current_user
import os
from werkzeug.utils import secure_filename

# Regex for email validation
EMAIL_PATTERN = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

# Reggex for password validation
PASSWORD_LENGTH_PATTERN = r'^.{8,}$'
PASSWORD_SPECIAL_CHARACTER_PATTERN = r'[!@#$%^&*(),.?":{}|<>]'
PASSWORD_NUMBER_PATTERN = r'\d'

# Allowed extensions for picture uploading
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Default picture for users without a pic configured in the profile
DEFAULT_PIC = 'default.png'


def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    file_extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else None
    return '.' in filename and file_extension in allowed_extensions


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        last_name = data.get('last_name')
        phone_number = data.get('phone_number')
        telegram_user = data.get('telegram_user')

        if not email or not password or not name or not last_name:
            return jsonify({'message': 'Missing required fields (email, username, password, name, or last_name)'}), 400

        if not re.match(EMAIL_PATTERN, email):
            return jsonify({'message': 'Invalid email format'}), 400

        app.logger.info(f"Received registration request for email: {email}")
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(email=email, username=email, password=hashed_password, name=name, last_name=last_name,
                        phone_number=phone_number, telegram_user=telegram_user)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'}), 201
    except IntegrityError as e:
        app.logger.warning(f"Registration failed due to IntegrityError: {e}")
        db.session.rollback()
        if 'email' in e.orig.args[0]:
            return jsonify({'message': 'Email already exists'}), 400
        elif 'username' in e.orig.args[0]:
            return jsonify({'message': 'Username already exists'}), 400
        else:
            return jsonify({'message': 'Registration failed due to a database error'}), 500
    except Exception as e:
        app.logger.error(f"Registration failed due to an unexpected error: {e}")
        db.session.rollback()
        return jsonify({'message': 'Registration failed due to an unexpected error'}), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        data = request.get_json(force=True)
        email_or_username = data.get('email') or data.get('username')
        password = data.get('password')

        user_db = User.query.filter(
            db.or_(User.email == email_or_username, User.username == email_or_username)
        ).first()

        if not user_db or not check_password_hash(user_db.password, password):
            return jsonify({'message': 'Invalid email/username or password'}), 401

        login_user(user_db)

        return jsonify({'logged': 'successful'}), 200

    except Exception as e:
        app.logger.warning(e)
        return jsonify({'message': 'Internal Server Error. Ask the administrator'}), 500


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    try:
        logout_user()
        return redirect(url_for('index'))
    except Exception as e:
        app.logger.error(e)
        raise


@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    try:
        user = current_user
        data = request.form
        new_name = data.get('name')
        new_last_name = data.get('last_name')
        new_telegram_user = data.get('telegram_user')
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if old_password and (not new_password or not confirm_password):
            return jsonify({'message': 'New password and confirmation are required when changing the password'}), 400

        if old_password and not check_password_hash(user.password, old_password):
            return jsonify({'message': 'Incorrect old password'}), 400

        if new_password != confirm_password:
            return jsonify({'message': 'New password fields do not match'}), 400

        if new_password and not (
            re.search(PASSWORD_LENGTH_PATTERN, new_password) and
            re.search(PASSWORD_SPECIAL_CHARACTER_PATTERN, new_password) and
            re.search(PASSWORD_NUMBER_PATTERN, new_password) and
            new_password != old_password
        ):
            return jsonify({
                'message': 'Invalid new password. Password must be at least 8 characters long, '
                           'contain at least one special character, one number, and must not be '
                           'the same as the old password'
            }), 400

        # Update user data
        user.name = new_name if new_name else user.name
        user.last_name = new_last_name if new_last_name else user.last_name
        user.telegram_user = new_telegram_user if new_telegram_user else user.telegram_user

        # Update password if a new one is provided
        if new_password:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')

        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                app.logger.warning(file_path)
                file.save(file_path)
                app.logger.warning(file_path)
                user.profile_picture = filename

        db.session.commit()

        # Return the updated user data
        return jsonify({
            'name': user.name,
            'last_name': user.last_name,
            'telegram_user': user.telegram_user,
            'email': user.email,
            'username': user.username
        }), 200
    except Exception as e:
        app.logger.warning(str(e))
        db.session.rollback()
        return jsonify({'message': 'Internal Server Error. Ask the administrator'}), 500
