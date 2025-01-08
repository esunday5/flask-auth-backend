from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required
from flask_migrate import Migrate
from config import Config
from dotenv import load_dotenv
import pg8000

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()

def log_request_info(app):
    """Middleware to log request details."""
    @app.before_request
    def before_request():
        print(f"Request: {request.method} {request.path}")
        print(f"Headers: {request.headers}")

def validate_auth_header(app):
    """Middleware to validate Authorization header."""
    @app.before_request
    def before_request():
        if not request.headers.get("Authorization"):
            return {"error": "Authorization header missing"}, 401

def create_app():
    """Factory function to create Flask app."""
    app = Flask(__name__)
    app.config.from_object(Config)

    # JWT secret key
    app.config['JWT_SECRET_KEY'] = 'xyzadmin@it'
    jwt.init_app(app)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Load environment variables
    load_dotenv()

    # Apply middleware
    log_request_info(app)
    validate_auth_header(app)

    # Test database connection
    try:
        connection = pg8000.connect(
            database="ekondo",
            user="admin",
            password="aZ2ryQ9DACsQNFDY1tQouCigbOO8N2ib",
            host="dpg-ctpbp40gph6c73dcjppg-a.oregon-postgres.render.com",
            port=5432
        )
        print("Database connection successful!")
        connection.close()
    except Exception as e:
        print(f"Database connection error: {e}")

    # Register blueprints
    from routes import auth, main
    app.register_blueprint(auth, url_prefix='/api/auth')
    app.register_blueprint(main, url_prefix='/main')

    # Example route to verify the JWT setup
    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        return jsonify(message="This is a protected route")

    return app
