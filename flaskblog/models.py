import logging
from datetime import datetime
from flaskblog import db, login_manager, bcrypt
from flask_login import UserMixin
from sqlalchemy.exc import DataError, IntegrityError, SQLAlchemyError

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class AuthService:
    """Encapsulates user authentication, password validation, and database error handling."""

    def __init__(self, db_session=None, hasher=None):
        self.db = db_session or db
        self.hasher = hasher or bcrypt

    def authenticate_user(self, email: str, password: str) -> tuple[dict, int]:
        """
        Validates user credentials against the database.
        Returns a tuple of (response_dict, http_status_code).
        """
        if not email or not isinstance(email, str):
            return {"success": False, "message": "Email must be a non-empty string"}, 422

        if not password or not isinstance(password, str):
            return {"success": False, "message": "Password must be a non-empty string"}, 422

        try:
            user = User.query.filter_by(email=email.strip().lower()).first()

            if user and self.hasher.check_password_hash(user.password, password):
                return {"success": True, "redirect_url": "home"}, 200
            
            return {"success": False, "message": "Invalid email or password."}, 401

        except DataError as e:
            self.db.session.rollback()
            logging.error(f"Data Overflow/Error: {e}")
            return {"success": False, "message": "Input value exceeds allowable database limits"}, 400

        except IntegrityError as e:
            self.db.session.rollback()
            logging.error(f"Integrity Error: {e}")
            return {"success": False, "message": "Database constraint violation"}, 409

        except SQLAlchemyError as e:
            self.db.session.rollback()
            logging.exception(f"Database Error: {e}")
            return {"success": False, "message": "Database error occurred. Please try again."}, 500

        except Exception as e:
            self.db.session.rollback()
            logging.exception(f"Unexpected Backend Error: {e}")
            return {"success": False, "message": "An internal server error occurred"}, 500