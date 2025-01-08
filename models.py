from app_config import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))

    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    branch = db.relationship('Branch', backref=db.backref('users', lazy=True))
    department = db.relationship('Department', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        """Hashes the password and stores it in the password_hash field."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Checks if the provided password matches the stored password hash."""
        return bcrypt.check_password_hash(self.password_hash, password)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"

class Branch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Branch {self.name}>"

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'))

    branch = db.relationship('Branch', backref=db.backref('departments', lazy=True))

    def __repr__(self):
        return f"<Department {self.name}>"
