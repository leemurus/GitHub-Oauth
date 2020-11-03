import datetime

from flask_login import UserMixin

from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.Integer)
    social_name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256))
    login = db.Column(db.String(256), nullable=False)
    avatar_url = db.Column(db.String(256))
    numbers = db.relationship('Number', backref='user', lazy=True)

    def set_generate_numbers(self, value):
        self.generate_numbers = value
        self.commit_to_db()

    def add_number(self, number):
        number_model = Number(number=number, user_id=self.id)
        number_model.commit_to_db()

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


class Number(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def commit_to_db(self):
        db.session.add(self)
        db.session.commit()


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
