from app_config import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f"<Role {self.name}>"

class Branch(db.Model):
    __tablename__ = 'branches'  # Ensuring this matches the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    # Relationship with Department
    departments = db.relationship('Department', back_populates='branch', lazy=True)

    def __repr__(self):
        return f"<Branch {self.name}>"

class Department(db.Model):
    __tablename__ = 'departments'  # Ensuring this matches the table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)

    # Relationship to Branch
    branch = db.relationship('Branch', back_populates='departments')

    def __repr__(self):
        return f"<Department {self.name}>"

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('branches.id'), nullable=False)  # Corrected ForeignKey reference
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)  # Corrected ForeignKey reference

    role = db.relationship('Role', backref='users')
    branch = db.relationship('Branch', backref='users')
    department = db.relationship('Department', backref='users')

    def __repr__(self):
        return f"<User {self.username}>"

    # Add set_password method to hash the password before saving
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Add check_password method to verify the password during login
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
