"""Models and database functions for final project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import json
from datetime import datetime, timedelta
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """User of campsite notifier website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(10))
    request = db.relationship("Request")

    def __repr__(self):

        return f"<User user_id={self.user_id}>"


class Campsite(db.Model):

    __tablename__ = "campsites"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    park = db.Column(db.String(250))

    def __repr__(self):

        return f"<Campsite id={self.id} name={self.name}>"


class Request(db.Model):
    """Request on campsite notifier website"""

    __tablename__ = "campsite_requests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    campsite_id = db.Column(db.String, db.ForeignKey("campsites.id"))
    date_start = db.Column(db.DateTime)
    date_end = db.Column(db.DateTime)
    available = db.Column(db.Boolean, default=False)
    sms_sent = db.Column(db.Boolean, default=False)
    user = db.relationship("User")

    def __repr__(self):

        return f"""<Request id={self.id} user_id={self.user_id} campsite_id={self.campsite_id} available={self.available}>"""


def connect_to_db(app):
    """Connect to database"""

    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///camping"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False

    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from server import app

    connect_to_db(app)
    print("Connected to DB.")
