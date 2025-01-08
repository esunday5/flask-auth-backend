from flask import Blueprint, request, jsonify
from app_config import db
from models import User
from flask_jwt_extended import jwt_required, create_access_token, JWTManager
import pg8000

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)

# Ensure JWT Manager is initialized in your app configuration
jwt = JWTManager()

# Custom error handling for missing Authorization header
@jwt.unauthorized_loader
def missing_token_error(error):
    return jsonify({"error": "Authorization header missing"}), 401


@auth.route('/register', methods=['POST'])
def register():
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


@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username_or_email = data.get('username_or_email')
    password = data.get('password')

    user = User.query.filter((User.username == username_or_email) | (User.email == username_or_email)).first()

    if user and user.check_password(password):
        token = create_access_token(identity=user.id)  # Create a token for the logged-in user
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid credentials'}), 401


@main.route('/users', methods=['GET'])
@jwt_required()  # Ensure the route is protected by JWT
def get_users():
    users = User.query.all()
    return jsonify([{
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role.name if user.role else None,
        "branch": user.branch.name if user.branch else None,
        "department": user.department.name if user.department else None
    } for user in users])


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
        return {"error": str(e)}, 500
