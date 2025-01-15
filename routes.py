from flask import Blueprint, request, jsonify
from app_config import db
from models import User
from flask_jwt_extended import create_access_token
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from sqlalchemy.orm.exc import NoResultFound
import pg8000

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
bcrypt = Bcrypt()

@auth.route('/register', methods=['POST'])
def register():
    try:
        # Get the data from the request
        data = request.get_json()
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        role_id = data.get('role_id')
        branch_id = data.get('branch_id')
        department_id = data.get('department_id')

        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Create new user
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            role_id=role_id,
            branch_id=branch_id,
            department_id=department_id
        )
        new_user.set_password(password)  # Set the password hash

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'message': 'Error: Integrity error, check foreign key constraints or unique constraints.'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error: {str(e)}'}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # Check if the user exists by username or email
        user = None
        if '@' in username_or_email:  # Check if it's an email
            user = User.query.filter_by(email=username_or_email).first()
        else:  # Else, treat it as a username
            user = User.query.filter_by(username=username_or_email).first()

        # If user does not exist
        if user is None:
            return jsonify({'message': 'User not found'}), 404

        # Check the password
        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({'message': 'Invalid password'}), 401

        # Optionally, create JWT token
        access_token = create_access_token(identity=user.id)

        # Return the user's role and JWT token
        return jsonify({
            'message': 'Login successful',
            'role': user.role.name,  # Assuming role has a 'name' field
            'access_token': access_token,  # You can include this token for future authenticated requests
            'expires_in': 24 * 60 * 60  # 24 hours in seconds
        }), 200

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500


@main.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@main.route('/test-db-connection', methods=['GET'])
def test_db_connection():
    try:
        connection = pg8000.connect(
            user="admin",
            password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
            host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
            port=5432,
            database="ekondo"
        )
        connection.close()
        return {"message": "Database connection successful!"}, 200
    except Exception as e:
        return {"error": f"Database connection error: {str(e)}"}, 500

@auth.route('/get_role', methods=['POST'])
def get_role():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Find user by email or username
        user = User.query.filter(
            (User.username == email) | (User.email == email)
        ).first()

        if user and user.check_password(password):  # Check password match
            return jsonify({'role': user.role.name}), 200  # Return role
        else:
            return jsonify({'role': None}), 404  # If no match found, return null

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

