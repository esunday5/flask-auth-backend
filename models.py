from app_config import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    branch = db.relationship('Branch', backref=db.backref('users', lazy=True))
    department = db.relationship('Department', backref=db.backref('users', lazy=True))

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
