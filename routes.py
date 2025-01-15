from flask import Blueprint, request, jsonify
from app_config import db
from models import User
from flask_jwt_extended import create_access_token
import pg8000

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

@auth.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username_or_email = data.get('username_or_email')
        password = data.get('password')

        # Fetch the user by username or email with the role eagerly loaded
        user = User.get_user_by_credentials(username_or_email)

        if user and user.check_password(password):
            # Create the access token for the user
            token = create_access_token(identity=user.id)
            expires_in = 24 * 60 * 60  # 24 hours in seconds
            return jsonify({'token': token, 'expires_in': expires_in, 'role': user.role}), 200  # Return the role as well

        return jsonify({'message': 'Invalid credentials'}), 401
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

        # Find user by email
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):  # Check password match
            return jsonify({'role': user.role.name}), 200  # Return role
        else:
            return jsonify({'role': None}), 404  # If no match found, return null
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500
